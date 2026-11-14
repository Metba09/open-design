## Code Context

**Query:** comment l'interface web communique avec le daemon

### Entry Points

- **COMMENT** (constant) - apps/web/src/collab/CommentDriftDemo.tsx:14
  `= {
  id: 'c-demo',
  filePath: 'index.html',
  elementId: 'el-headline',
  selector: '.headline',
  h...`
- **CommentSyncScope** (interface) - apps/daemon/src/collab/comment-sync-state.ts:10
- **CommentFileFact** (interface) - packages/contracts/src/api/comments.ts:114

### Related Symbols

- packages/contracts/src/api/comments.ts: PreviewComment:141
- apps/web/src/collab/CommentDriftDemo.tsx: CommentDriftDemo:92
- apps/daemon/src/collab/comment-alignment.ts: key:131
- apps/daemon/src/collab/comment-sync-state.ts: args:29, createCommentSyncStateService:19, read:34, retry:13, read:12
- apps/daemon/tests/comment-file-facts.test.ts: fact:10
- apps/daemon/src/collab/comment-file-deletion.ts: reconcile:75

### Code

#### COMMENT (apps/web/src/collab/CommentDriftDemo.tsx:14)

```tsx
const COMMENT: PreviewComment = {
  id: 'c-demo',
  filePath: 'index.html',
  elementId: 'el-headline',
  selector: '.headline',
  htmlHint: '<h1 class="headline">',
  text: 'Tighten this headline',
  position: { x: 40, y: 30, width: 300, height: 48 },
  anchoredVersion: 1,
  createdAt: 1,
} as PreviewComment;
```

#### CommentSyncScope (apps/daemon/src/collab/comment-sync-state.ts:10)

```typescript
export interface CommentSyncScope { projectId: string; workspaceId: string; workspaceMemberId: string; filePath?: string }
```

#### CommentFileFact (packages/contracts/src/api/comments.ts:114)

```typescript
export interface CommentFileFact {
  sourceFileId: string;
  sourceFilePath: string;
  entryPath: string;
  resourceId: string;
  versionId: string;
  retired: boolean;
}
```

#### CommentDriftDemo (apps/web/src/collab/CommentDriftDemo.tsx:92)

```tsx
export function CommentDriftDemo() {
  const [scenarioKey, setScenarioKey] = useState(SCENARIOS[0]!.key);
  const scenario = SCENARIOS.find((s) => s.key === scenarioKey) ?? SCENARIOS[0]!;

  const resolution = useMemo(
    () => resolveCommentAnchor(COMMENT, scenario.snapshots, scenario.currentVersion),
    [scenario],
  );
  const writeBacks = useMemo(
    () => planLostAnchorWriteBacks([{ comment: COMMENT, resolution }]),
    [resolution],
  );

  return (
    <div className={styles.session}>
      <div className={styles.row}>
        <strong>Comment drift ladder</strong>
        <span className={styles.count}>real engine · synthetic snapshots</span>
      </div>

      <div className={styles.scenarioBtns}>
        {SCENARIOS.map((s) => (
          <button
            key={s.key}
            type="button"
            className={s.key === scenarioKey ? styles.scenarioActive : ''}
            onClick={() => setScenarioKey(s.key)}
          >
            {s.label}
          </button>
        ))}
      </div>

      <p className={styles.note}>{scenario.note}</p>

      <div className={styles.row}>
        <span className={styles.label}>Resolved state</span>
        <span className={styles.badge} data-anchor-state={resolution.state}>
          {STATE_LABEL[resolution.state] ?? resolution.state}
        </span>
      </div>

      <div className={styles.row}>
        <span className={styles.label}>Anchored to</span>
        <code className={styles.mono}>
          {resolution.sna
... (truncated) ...
```

#### key (apps/daemon/src/collab/comment-alignment.ts:131)

```typescript
  const key = (scope: CommentSyncScope) => JSON.stringify([scope.projectId, scope.workspaceId, scope.workspaceMemberId]);
```

