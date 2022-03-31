<template>
  <div>
      <section v-show="!explanation" class="xd-section xd-light" >
         <section v-show="!user_city_answer">
            {{ msg }}
         </section>   
      <section v-show="user_city_answer && !prediction_city">
        <p class="short-text">Your guess is: {{user_city_answer}}</p>
      </section>
      <section v-show="prediction_city && control">
        <p class="short-text">My guess is: {{prediction_city}}</p>
      </section>
        <section v-show="prediction_city && !control">
        <p>My guess is: {{prediction_city}}
        <br>In particular, the colored areas below have helped me form my guess. </p>
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
       label_city: {
          type: String
      },
      user_city_answer: {
          type: String
      },
      prediction_city: {
        type: String
      },
  control:{
        type: Boolean
      },
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
.short-text{
  line-height: 2;
}

</style>
