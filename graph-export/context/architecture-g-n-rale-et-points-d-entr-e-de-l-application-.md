## Code Context

**Query:** architecture générale et points d'entrée de l'application

### Entry Points

- **ReferralEntry** (function) - apps/web/src/components/ReferralEntry.tsx:39
  `({ compact = false }: { compact?: boolean })`
- **ReferralEntryProvider** (function) - apps/web/src/components/ReferralEntry.tsx:12
  `({ accountId, profile, children }: { accountId: string | null; profile: string | null; children: ReactNode })`
- **OnboardingEntry** (interface) - apps/web/src/onboarding/onboarding-entry.ts:24

### Related Symbols

- apps/web/src/components/ReferralEntry.tsx: open:49, ReferralEntryContext:10, read:20
- apps/web/src/components/referral-entry-copy.ts: getReferralEntryCopy:22
- apps/web/src/i18n/index.tsx: useI18n:259
- apps/web/src/analytics/referral.ts: useReferralAnalytics:8
- apps/web/src/components/EntryNavRail.tsx: EntryNavRail:1978
- apps/web/tests/components/ReferralEntry.test.tsx: view:47
- apps/web/src/App.tsx: AppInner:997
- apps/web/src/components/RecommendedStartRegion.tsx: handleEnter:108

### Code

#### ReferralEntry (apps/web/src/components/ReferralEntry.tsx:39)

```tsx
export function ReferralEntry({ compact = false }: { compact?: boolean }) {
  const { active, profile, scopeKey } = useContext(ReferralEntryContext);
  const { locale, t } = useI18n();
  const [failed, setFailed] = useState(false);
  const currentScope = useRef(scopeKey);
  currentScope.current = scopeKey;
  useEffect(() => setFailed(false), [scopeKey, active]);
  const analytics = useReferralAnalytics<HTMLButtonElement>('client_entry', active && !compact ? scopeKey : null);
  if (!active || compact) return null;
  const [title, subtitle] = getReferralEntryCopy(locale);
  const open = async () => {
    analytics.click('invite');
    try {
      const accepted = await openReferralActivity(profile, 'client_entry', () => currentScope.current === scopeKey);
      if (currentScope.current === scopeKey) setFailed(!accepted);
    } catch { if (currentScope.current === scopeKey) setFailed(true); }
  };
  return <div className={styles.slot}><button ref={analytics.ref} type="button" className={styles.card} data-testid="referral-entry" aria-label={`${title} — ${subtitle}`} title={`${title} — ${subtitle}`} onClick={() => void open()}><span className={styles.art} aria-hidden="true" /><span className={styles.copy}><strong>{title}</strong><span>{subtitle}</span></span></button>{failed ? <span role="alert">{t('referral.notice.openFailed')}</span> : null}</div>;
}
```

#### ReferralEntryProvider (apps/web/src/components/ReferralEntry.tsx:12)

```tsx
export function ReferralEntryProvider({ accountId, profile, children }: { accountId: string | null; profile: string | null; children: ReactNode }) {
  const [result, setResult] = useState<{ key: string; active: boolean } | null>(null);
  const key = `${profile}:${accountId}`;
  useEffect(() => {
    if (!accountId) return;
    const controller = new AbortController();
    let current = true;
    let generation = 0;
    const read = async () => {
      const request = ++generation;
      try {
        const response = await fetch('/api/integrations/vela/referral-summary', { cache: 'no-store', signal: controller.signal });
        if (!response.ok) throw new Error('unavailable');
        const data = parseReferralSummary(await response.json());
        if (current && request === generation) setResult({ key, active: data?.campaignStatus === 'active' });
      } catch {
        if (current && request === generation) setResult({ key, active: false });
      }
    };
    void read();
    const timer = window.setInterval(() => void read(), 30_000);
    window.addEventListener('focus', read);
    return () => { current = false; controller.abort(); window.clearInterval(timer); window.removeEventListener('focus', read); };
  }, [accountId, key]);
  return <ReferralEntryContext.Provider value={{ active: Boolean(accountId && result?.key === key && result.active), profile, scopeKey: key }}>{children}</ReferralEntryContext.Provider>;
}
```

#### OnboardingEntry (apps/web/src/onboarding/onboarding-entry.ts:24)

```typescript
export interface OnboardingEntry {
  source: 'home_recommendation';
  productType: ProductType;
  recommendationId: string;
  // Survey answers that produced the recommendation, echoed on the
  // `onboarding_prompt_prefilled` funnel event (spec §11.1). Analysis-only —
  // they live in this session slot, never in project data.
  role?: string;
  useCases?: string[];
  // The prompt the recommendation prefilled into the Studio composer, captured
  // at create time. Cached WITH the entry so it survives ProjectView remounts:
  // `project.pendingPrompt` is wiped by `onClearPendingPrompt()` on the first
  // mount, so a reopen-before-send would otherwise lose the comparison base and
  // report `has_prefilled_prompt=false` even when the user sends the original
  // recommended draft unchanged (spec §7.4 / §8.2).
  seedPrompt?: string;
}
```

#### open (apps/web/src/components/ReferralEntry.tsx:49)

```tsx
  const open = async () => {
    analytics.click('invite');
    try {
      const accepted = await openReferralActivity(profile, 'client_entry', () => currentScope.current === scopeKey);
      if (currentScope.current === scopeKey) setFailed(!accepted);
    } catch { if (currentScope.current === scopeKey) setFailed(true); }
  };
```

#### getReferralEntryCopy (apps/web/src/components/referral-entry-copy.ts:22)

```typescript
export function getReferralEntryCopy(locale: string): readonly [string, string] {
  return referralEntryCopy[locale] ?? referralEntryCopy[locale.split('-')[0] ?? ''] ?? ['Share OpenDesign', 'Earn reset cards'];
}
```

