<template>
  <div class="selection">
    <section class="xd-section xd-light">
      <div v-for="city in cities" :key="city.city" class="element">
        <input
          type="Button"
          class="xd-button xd-secondary"
          :value="city.city"
          @click="selectCity(city.city)"
        />
      </div>
    </section>
  </div>
</template>
<script>
export default {
  name: "CitySelector",
  emits: ["citySelected"],
  data() {
    return {
      /* TODO: Load this from config */
      cities: [
        {
          city: "Tel Aviv",
          backend: "Tel_Aviv",
        },
        {
          city: "Jerusalem",
          backend: "Westjerusalem",
        },
        {
          city: "Berlin",
          backend: "Berlin",
        },
        {
          city: "Hamburg",
          backend: "Hamburg",
        },
      ],
    };
  },

  computed: {},
  methods: {
    selectCity(city) {
      this.$emit("citySelected", city);
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
