import { useState } from "nuxt/app"

export const useLeftCollapsed = () => {
    return useState<boolean>("leftCollapsed", () => false)
  }
  