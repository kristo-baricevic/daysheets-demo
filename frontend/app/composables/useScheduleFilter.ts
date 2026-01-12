export type ScheduleAssocPick = {
  key: string;
  kind: "person" | "group";
  id: string;
  label: string;
  kindLabel: string;
};

export const useScheduleFilterOpen = () => useState<boolean>("scheduleFilterOpen", () => false);

export const useScheduleAssoc = () =>
  useState<ScheduleAssocPick | null>("scheduleAssoc", () => null);
