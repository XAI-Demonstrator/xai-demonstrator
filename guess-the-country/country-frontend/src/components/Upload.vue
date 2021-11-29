<template>
  <div class="container">
    <div class="large-12 medium-12 small-12 cell">
      <label>File
         <input type="file" @change="handleFileUpload( $event )"/>
      </label>
        <button v-on:click="submitFile()">Submit</button>
    </div>
  </div>
</template>
<script>
import axios from 'axios';
  export default {
    name: 'Upload',
    data(){
  return {
    file: ''
  }
},
    methods: {
      handleFileUpload(event){
            this.file = event.target.files[0];
      },
      submitFile(){
          let formData = new FormData();
          formData.append('file', this.file);
            axios.post( '/predict/image3',
            formData,
            {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }
            ).then(function(){
            console.log('SUCCESS!!');
            })
            .catch(function(){
            console.log('FAILURE!!');
            });
    },
    }
  }
</script>