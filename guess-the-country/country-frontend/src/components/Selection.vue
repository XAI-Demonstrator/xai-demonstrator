<template>
  <div>
    <section
      v-if="!user_country_answer"
      class="flex-style xd-section xd-light"
    >
      <div v-for="country in countrys" :key="country.country" class="element">
        <input
          type="Button"
          class="xd-button xd-secondary"
          v-bind:value="country.country"
          v-on:click="answer_country(country.country)"
        />
      </div>
    </section>

    <section
      v-if="user_country_answer && !user_city_answer"
      class="xd-section xd-light"
  
    >
      <div v-for="country in countrys" :key="country.citys">
        <div v-if="country.country == label_country" class="flex-style">
          <div v-for="city in country.citys" :key="city.city" class="element">
            <input
          type="Button"
          class="xd-button xd-secondary"
          v-bind:value="city.city"
          v-on:click="answer_city(city.city)"
        />
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
<script>
export default {
  name: "Selection",
  props: {
    label_country: {
      type: String,
    },
    user_country_answer: {
      type: String,
    },
    user_city_answer: {
      type: String,
    },
  },
  data() {
    return {
      countrys: [
        {
          country: "Israel",
          citys: [
            {
              city: "Tel Aviv",
              backend: "Tel_Aviv",
            },
            {
              city: "Westjerusalem",
              backend: "Westjerusalem",
            },
          ],
        },
        {
          country: "Germany",
          citys: [
            {
              city: "Berlin",
              backend: "Berlin",
            },
            {
              city: "Hamburg",
              backend: "Hamburg",
            },
          ],
        },
      ],
    };
  },
  methods: {
    answer_country(country) {
      this.$emit("country_selected", country);
    },
    answer_city(city) {
      this.$emit("city_selected", city);
    },
  },
};
</script>
<style scoped>
.element {
  flex: 1;
}
.flex-style {
display: flex; 
gap: 10px
}
.xd-section:last-child {
  margin-bottom: 12px;
}
</style>
