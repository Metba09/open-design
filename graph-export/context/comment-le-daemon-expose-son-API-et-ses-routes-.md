## Code Context

**Query:** comment le daemon expose son API et ses routes

### Entry Points

- **Routine** (interface) - apps/daemon/src/routines.ts:48
- **Routine** (interface) - packages/contracts/src/api/routines.ts:92
- **CommentFileFact** (interface) - packages/contracts/src/api/comments.ts:114

### Related Symbols

- apps/daemon/tests/routines.test.ts: fixtureRoutine:66, list:38, constructor:36
- apps/daemon/src/routines.ts: scheduleRoutine:498, list:119, scheduleRoutineAt:512, RoutineRunHandler:111
- apps/daemon/tests/comment-file-facts.test.ts: fact:10
- apps/daemon/src/collab/comment-file-deletion.ts: reconcile:75
- apps/daemon/src/collab/comment-file-authority.ts: retiredCommentFileMutation:66

### Code

#### Routine (apps/daemon/src/routines.ts:48)

```typescript
export interface Routine {
  id: string;
  name: string;
  prompt: string;
  schedule: RoutineSchedule;
  target: RoutineProjectTarget;
  skillId: string | null;
  agentId: string | null;
  context: RoutineContextSelection;
  enabled: boolean;
  nextRunAt: number | null;
  lastRun: unknown;
  createdAt: number;
  updatedAt: number;
}
```

#### Routine (packages/contracts/src/api/routines.ts:92)

```typescript
export interface Routine {
  id: string;
  name: string;
  prompt: string;
  schedule: RoutineSchedule;
  target: RoutineProjectTarget;
  skillId: string | null;
  agentId: string | null;
  context?: RoutineContextSelection;
  enabled: boolean;
  nextRunAt: number | null;
  lastRun: RoutineLastRunSummary | null;
  createdAt: number;
  updatedAt: number;
}
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

#### fixtureRoutine (apps/daemon/tests/routines.test.ts:66)

```typescript
function fixtureRoutine(overrides: Partial<Routine> = {}): Routine {
  return {
    id: 'routine-1',
    name: 'Daily brief',
    prompt: 'Summarize the day',
    schedule: { kind: 'hourly', minute: 1 },
    target: { mode: 'create_each_run' },
    skillId: null,
    agentId: null,
    context: {},
    enabled: true,
    nextRunAt: null,
    lastRun: null,
    createdAt: Date.UTC(2026, 4, 17, 0, 0),
    updatedAt: Date.UTC(2026, 4, 17, 0, 0),
    ...overrides,
  };
}
```

#### scheduleRoutine (apps/daemon/src/routines.ts:498)

```typescript
  private scheduleRoutine(routine: Routine): void {
    if (!routine.enabled) return;
    const fireAt = nextRunAtForSchedule(routine.schedule);
    if (!fireAt) return;
    this.scheduleRoutineAt(routine, fireAt);
  }
```

