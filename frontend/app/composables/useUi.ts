import { useState } from "nuxt/app";

// composables/useUi.ts
export const useLeftCollapsed = () => useState<boolean>("leftCollapsed", () => false);
