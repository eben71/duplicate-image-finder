export const keys = { Keep: "k", Delete: "d", Skip: "s" } as const;
export type KeyboardAction = keyof typeof keys;
