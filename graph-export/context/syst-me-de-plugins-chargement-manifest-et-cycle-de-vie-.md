## Code Context

**Query:** système de plugins : chargement, manifest et cycle de vie

### Entry Points

- **PluginsViewProps** (interface) - apps/web/src/components/PluginsView.tsx:221
- **handleView** (function) - apps/web/src/components/DesignSystemPreviewModal.tsx:100
  `(viewId: string)`
- **PluginsView** (function) - apps/web/src/components/PluginsView.tsx:241
  `({
  onCreatePlugin,
  onUsePlugin,
  onCreatePluginShareProject,
}: PluginsViewProps)`

### Related Symbols

- apps/web/src/components/DesignSystemPreviewModal.tsx: DesignSystemPreviewModal:46
- apps/web/src/collab/workspace-identity.ts: beginWorkspaceResourceScopedRead:181, isStillCurrent:177
- apps/web/src/providers/registry.ts: fetchDesignSystemPreview:3658, fetchDesignSystemShowcase:3677
- apps/web/src/analytics/events.ts: trackDesignSystemsTemplatesModalClick:755
- apps/web/src/components/PluginsView.tsx: refresh:316, handleMarketplaceMutation:500, handleDuplicatePlugin:429, requestPluginShareTask:478

### Code

#### PluginsViewProps (apps/web/src/components/PluginsView.tsx:221)

```tsx
interface PluginsViewProps {
  onCreatePlugin?: (goal?: string) => void;
  onUsePlugin?: (record: InstalledPluginRecord, action: PluginUseAction) => void;
  onCreatePluginShareProject?: (
    pluginId: string,
    action: PluginShareAction,
    locale?: string,
  ) => Promise<PluginShareProjectOutcome>;
}
```

#### handleView (apps/web/src/components/DesignSystemPreviewModal.tsx:100)

```tsx
    (viewId: string) => {
      if (initialViewIdRef.current === null) {
        initialViewIdRef.current = viewId;
      } else if (initialViewIdRef.current !== viewId) {
        initialViewIdRef.current = viewId;
        if (viewId === 'showcase' || viewId === 'kit' || viewId === 'tokens') {
          trackDesignSystemsTemplatesModalClick(analytics.track, {
            page_name: 'design_systems',
            area: 'templates_modal',
            element: viewId === 'kit' ? 'open_design_set' : viewId,
            templates_id: system.id,
            templates_type: system.source ?? 'library',
          });
        }
      }
      if (viewId === 'showcase' && showcaseHtml === undefined) {
        const read = beginWorkspaceResourceScopedRead(resourceReadIdentityRef.current);
        setShowcaseHtml(null);
        void fetchDesignSystemShowcase(system.id, read.context).then((html) => {
          if (read.isStillCurrent(resourceReadIdentityRef.current)) setShowcaseHtml(html);
        });
      }
      if (viewId === 'tokens' && tokensHtml === undefined) {
        const read = beginWorkspaceResourceScopedRead(resourceReadIdentityRef.current);
        setTokensHtml(null);
        void fetchDesignSystemPreview(system.id, read.context).then((html) => {
          if (read.isStillCurrent(resourceReadIdentityRef.current)) setTokensHtml(html);
        });
      }
    },
```

#### PluginsView (apps/web/src/components/PluginsView.tsx:241)

```tsx
export function PluginsView({
  onCreatePlugin,
  onUsePlugin,
  onCreatePluginShareProject,
}: PluginsViewProps) {
  const { locale, t } = useI18n();
  const analytics = useAnalytics();
  // Attaches the same workspace identity headers project reads already carry
  // (`workspaceProjectHeaders`), so the daemon's `GET /api/plugins` /
  // `POST /api/plugins/install` can apply the workspace-scoped filter and
  // stamp new installs with the acting workspace. `useWorkspaceContext` is a
  // coalesced read shared across the nav shell, so calling it again here does
  // not fan out an extra fetch.
  const pluginsWorkspaceContextState = useWorkspaceContext();
  const {
    context: pluginsWorkspaceContext,
    loading: pluginsWorkspaceContextLoading,
    identityChangePending: pluginsIdentityChangePending,
    failure: pluginsWorkspaceContextFailure,
  } = pluginsWorkspaceContextState;
  const pluginsContextRef = useRef(pluginsWorkspaceContext);
  pluginsContextRef.current = pluginsWorkspaceContext;
  const pluginsAccountGeneration = currentWorkspaceAccountGeneration();
  const pluginsReadMode: PluginWorkspaceReadMode = pluginsIdentityChangePending
    || (!pluginsWorkspaceContext && pluginsWorkspaceContextLoading)
    ? 'pending'
    : pluginsWorkspaceContext
      ? 'scoped'
      : pluginsWorkspaceContextFailure === 'unavailable'
        ? 'blocked'
        : 'headerless';
  const pluginsIdentity = JSON.stringify([
    pluginsAccountGeneration,
    workspaceIdentityCacheKey(plu
... (truncated) ...
```

#### DesignSystemPreviewModal (apps/web/src/components/DesignSystemPreviewModal.tsx:46)

```tsx
export function DesignSystemPreviewModal({
  system,
  onClose,
  initialViewId = 'kit',
  workspaceContext: explicitWorkspaceContext,
  resourceReadIdentity: resourceReadIdentityProp,
}: Props) {
  const t = useT();
  const analytics = useAnalytics();
  const workspaceState = useWorkspaceContext();
  const ambientResourceReadIdentity = resolveWorkspaceResourceReadIdentity(workspaceState);
  const resourceReadIdentity = explicitWorkspaceContext !== undefined
    ? workspaceResourceReadIdentityFromContext(explicitWorkspaceContext)
    : resourceReadIdentityProp === undefined
      ? ambientResourceReadIdentity
      : resourceReadIdentityProp;
  const resourceReadIdentityKey = workspaceResourceReadIdentityKey(resourceReadIdentity);
  const resourceReadIdentityRef = useRef(resourceReadIdentity);
  resourceReadIdentityRef.current = resourceReadIdentity;
  const surfaceViewFiredRef = useRef<string | null>(null);
  useEffect(() => {
    if (surfaceViewFiredRef.current === system.id) return;
    surfaceViewFiredRef.current = system.id;
    trackDesignSystemsTemplatesModalSurfaceView(analytics.track, {
      page_name: 'design_systems',
      area: 'templates_modal',
      templates_id: system.id,
      templates_type: system.source ?? 'library',
    });
  }, [analytics.track, system.id, system.source]);

  const [showcaseHtml, setShowcaseHtml] = useState<string | null | undefined>(undefined);
  const [tokensHtml, setTokensHtml] = useState<string | null | undefined>(undefined);
  co
... (truncated) ...
```

#### beginWorkspaceResourceScopedRead (apps/web/src/collab/workspace-identity.ts:181)

```typescript
export function beginWorkspaceResourceScopedRead(
  identity: WorkspaceResourceReadIdentity | null | undefined,
): WorkspaceResourceScopedRead {
  const context = identity?.context ?? null;
  const key = workspaceResourceReadIdentityKey(identity);
  return {
    context,
    isStillCurrent: (current) => workspaceResourceReadIdentityKey(current) === key,
  };
}
```

