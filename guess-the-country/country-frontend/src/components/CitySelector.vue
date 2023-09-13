<template>
  <div class="selection">
    <section class="xd-section xd-light">
      <div v-for="city in cities" :key="city" class="element">
        <input
          type="button"
          class="xd-button xd-secondary"
          :value="city"
          @click="$emit('citySelected', city)"
        />
      </div>
    </section>
  </div>
</template>
<script>
import config from "@/assets/config.json";
export default {
  name: "CitySelector",
  emits: ["citySelected"],
  computed: {
    cities() {
      return Object.values(config).map((item) => item.city);
    },
  },
};
</script>
<style scoped>
.selection {
  width: 100%;
}

.element {
  margin-bottom: 10px;
}

.element:last-child {
  margin-bottom: 0;
}

.xd-section:last-child {
  margin-bottom: 12px;
}
</style>
