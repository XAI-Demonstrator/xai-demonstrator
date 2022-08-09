<template>
  <div>
      <section v-show="!explanation" class="xd-section xd-light" >
        <!-- Question -->
        <section v-show="sequence_mode==='classic'&&!user_city_answer
                  || sequence_mode==='recommender'&&!prediction_city
                  || sequence_mode==='basic'">  <!--ergänzen-->
            {{ msg }} 
        </section>   
        <!-- User guess -->
        <section v-show="sequence_mode==='classic'&&user_city_answer && !prediction_city
                  || sequence_mode==='recommender'&&user_city_answer
                  || sequence_mode==='basic'">  <!--ergänzen-->
          <p class="short-text">Your guess is: {{user_city_answer}}</p>
        </section>
        <!-- control group (without explanation), AI guess -->
        <section v-show="sequence_mode==='classic'&&prediction_city && control
                  || sequence_mode==='recommender'&& prediction_city&&!user_city_answer && control
                  || sequence_mode==='basic'"> <!--ergänzen-->
          <p class="short-text">My guess is: {{prediction_city}}</p>
        </section>
        <!-- treatment group (with explanation), AI guess -->
        <section v-show=" sequence_mode ==='classic' && prediction_city && !control
                  || sequence_mode==='recommender' &&prediction_city&&!user_city_answer && !control
                  || sequence_mode==='basic'"> <!--ergänzen--> 
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
      sequence_mode: {
        type: String
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
.short-text{
  line-height: 2;
}

</style>
