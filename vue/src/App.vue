<template>
  <div id="app">
    <router-view v-if="routerAlive"></router-view>
  </div>
</template>

<script>
import Home from '@/views/Home/index.vue'
export default {
  data(){
    return {
      routerAlive:true
    }
  },
  provide(){
    return {
      routerRefresh: this.routerRefresh
    }
  },
  methods:{
    routerRefresh(){
      this.routerAlive = false;
      this.$nextTick(()=>{
          this.routerAlive = true;
          // this.$router.push('/home')
      });
    },
  },
  components:{
    Home
  }
}
</script>

<style>

</style>
