<template>
  <div>
      <section v-show="!explanation" class="xd-section xd-light">
         <section v-show="!user_country_answer">
            {{ msg }}
         </section>   
        <section v-show="user_country_answer && !user_city_answer">
        <p v-if="user_country_answer == label_country" >Your answer: {{user_country_answer}} is right</p>
        <p v-else>Your answer: {{user_country_answer}} is wrong, the right answer ist: {{label_country}}</p>
      </section>
      <section v-show="user_city_answer && !prediction_city">
        <p v-if="user_city_answer == label_city" >Your answer: {{user_city_answer}} is right</p>
        <p v-else>Your answer: {{user_city_answer}} is wrong, the right answer ist: {{label_city}}</p>
      </section>
      <section v-show="prediction_city">
        <p v-if="prediction_city == label_city" >The AI answer: {{prediction_city}} is right</p>
        <p v-else>The AI answer: {{prediction_city}} is wrong, the right answer ist: {{label_city}}</p>
      </section>
    
      </section>
  </div>
</template>
<script>
export default {
  name: "Notification",
  props: {
      msg: {
          type: String,
          default: "Hello"
      },
      user_country_answer: {
          type: String
      },
      label_country: {
          type: String
      },
       label_city: {
          type: String
      },
      user_city_answer: {
          type: String
      },
      prediction_city: {
        type: String
      },
      explanation: {

      }
  },

 data() {
    return {
    }
 }
}
</script>
<style scoped>
.xd-section:last-child{
    text-align: center;
    margin-bottom: 12px;
}

</style>
