<template>
  <div>
    <section
      v-if="!user_country_answer"
      class="xd-section xd-light"
      id="radio_country"
      style="
        display: flex;
        align-content: flex-end;
        flex-wrap: wrap;
        align-items: baseline;
      "
    >
      <div v-for="country in countrys" :key="country.country">
        <input name="country" type="radio" v-bind:value="country.country" />
        <label>{{ country.country }}</label>
      </div>
      <button
        type="button"
        class="xd-button xd-secondary"
        style="width: auto; margin-left: auto"
        v-on:click="answer_country()"
      >
        Was I right?
      </button>
    </section>

    <section
      v-if="user_country_answer && !user_city_answer"
      class="xd-section xd-light"
      id="radio_city"
      style="
        display: flex;
        align-content: flex-end;
        flex-wrap: wrap;
        align-items: baseline;
      "
    >
      <div v-for="country in countrys" :key="country.citys">
        <div v-if="country.country == label_country">
          <div v-for="city in country.citys" :key="city.city">
            <input name="city" type="radio" v-bind:value="city.city" />
            <label>{{ city.city }}</label>
          </div>
        </div>
      </div>
      <button
        type="button"
        class="xd-button xd-secondary"
        style="width: auto; margin-left: auto"
        v-on:click="answer_city()"
      >
        Was I right?
      </button>
    </section>
  </div>
</template>
<script>
export default {
  name: "Selection",
  props: {
      label_country: {
          type: String
      },
      user_country_answer: {
        type: String
      },
      user_city_answer: {
        type: String
      }
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
    answer_city() {
      var radios = document.getElementsByName("city");

      for (var i = 0, length = radios.length; i < length; i++) {
        if (radios[i].checked) {
          this.$emit("city_selected", radios[i].value );
          break;
        }
      }
    },

    answer_country() {
      var radios = document.getElementsByName("country");

      for (var i = 0, length = radios.length; i < length; i++) {
        if (radios[i].checked) {
          this.$emit("country_selected", radios[i].value);
          break;
        }
      }
    },
  },
};
</script>
<style scoped>
.xd-section:last-child {
  margin-bottom: 12px;
}
</style>
