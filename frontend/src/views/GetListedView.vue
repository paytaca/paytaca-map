<template>
  <div class="h-full overflow-y-auto bg-cloud">
    <div class="mx-auto max-w-2xl px-6 py-16 text-center">
      <span class="mx-auto grid h-16 w-16 place-items-center rounded-3xl bg-brand-100 text-3xl shadow-card">🏪</span>
      <h1 class="mt-6 font-display text-3xl font-bold text-ink">Get Listed</h1>
      <p class="mt-3 text-ink-muted">
        Accept Bitcoin Cash through Paytaca and put your business on the map. Listing your shop is
        free — customers nearby will discover you and can pay in BCH.
      </p>
      <router-link
        to="/"
        class="mt-8 inline-flex items-center rounded-full bg-brand-600 px-5 py-2.5 text-sm font-semibold text-white shadow-pop hover:bg-brand-700"
      >
        Explore the map
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GetListedView',
}
</script>
