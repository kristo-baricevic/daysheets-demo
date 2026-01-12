export function usePeopleTableQuery() {
  const route = useRoute();
  const router = useRouter();

  const q = computed(() => String(route.query.q ?? ""));
  const status = computed(() => String(route.query.status ?? "all"));
  const sort = computed(() => String(route.query.sort ?? "name"));
  const dir = computed(() => String(route.query.dir ?? "asc"));
  const page = computed(() => {
    const n = Number(route.query.page ?? 1);
    return Number.isFinite(n) && n > 0 ? n : 1;
  });
  const pageSize = computed(() => {
    const n = Number(route.query.pageSize ?? 25);
    return Number.isFinite(n) && n > 0 ? n : 25;
  });

  function setQuery(patch: Record<string, string | number | null>) {
    const next: Record<string, any> = { ...route.query };
    for (const [k, v] of Object.entries(patch)) {
      if (v === null) delete next[k];
      else next[k] = String(v);
    }
    router.replace({ query: next });
  }

  return { q, status, sort, dir, page, pageSize, setQuery };
}
