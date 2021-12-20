<template>
  <div>
    <Header></Header>
    <div class="w">
      <div class="userhome w">
        <h1>用户画像</h1>
        <div class="userimg">
          <WordCloud></WordCloud>
        </div>
      </div>
      <div class="box w">
        <div class="box-hd">
          <h3>{{recommendType}}</h3>
          <!-- <a @click="changeMovies">换一批</a> -->
        </div>
        <div class="box-bd">
          <ul>
            <li v-for="item in displayList" :key="item.id">
              <a :href="'/single?movieid='+item.id" class="detail">
                <img :src="item.img" alt="">
                <div>
                  <h1>{{item.movie}}</h1>
                  <span class="name">{{item.director}}</span>
                  <span class="rate">{{item.rating}}</span>
                </div>
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios'
import WordCloud from '@/views/WordCloud/index.vue'
export default {
  name: 'UserPage',
  data() {
    return {
      count: 0,
      recommendType: '历史记录',
      displayList: [],
      username: sessionStorage.getItem('username'),
      
    }
  },
  components: {
    WordCloud
  },
  async mounted() {
    let result = await axios.get('/api/history', {
      params: { 'username': this.username }
    })
    if(result.data.msg=='success'){
      this.displayList=result.data.data
    }
    let result1 = await axios.get('/api/wordcloud', {
      params: { 'username': this.username }
    })
    if(result1.data.msg=='success'){
      this.worddata=result1.data.data
    }
    // console.log(result,result1)
  },
  methods: {}
}
</script>
<style lang='less' scoped>
.userhome h1 {
  margin-left: 100px;
  font-size: 20px;
  color: #494949;
  margin-bottom: 20px;
}
.userhome .userimg {
  margin-left: 100px;
  width: 400px;
  height: 300px;
}
a {
  display: block;
  text-decoration: none;
  color: #000;
  cursor: pointer;
}
.box {
  // float: left;
  margin-top: 30px;
}
.box-hd {
  height: 45px;
  margin-left: 100px;
}
.box-hd h3 {
  height: 45px;
  font-size: 20px;
  color: #494949;
  line-height: 45px;
  float: left;
}
.box-hd a {
  float: left;
  text-align: center;
  height: 43px;
  width: 58px;
  border: 1px solid silver;
  line-height: 43px;
  font-weight: 100;
  color: #a5a5a5;
  text-decoration: none;
  margin-left: 30px;
}
.box-hd a:hover {
  color: white;
  background-color: skyblue;
}
.box-bd ul {
  margin-left: 100px;
}
.box-bd ul li {
  float: left;
  width: 230px;
  height: 420px;
  // background-color: pink;
  margin-right: 15px;
  margin-top: 15px;
}
.box-bd li:hover {
  background-color: rgba(218, 217, 217, 0.7);
}
.box-bd ul li a img {
  display: block;
  width: 100%;
  height: 342px;
}
.box-bd ul li a h1 {
  font-size: 18px;
  font-weight: normal;
  margin: 5px 0px 5px 10px;
}
.name {
  float: left;
  margin-left: 10px;
  margin-top: 10px;
}
.rate {
  float: right;
  font-size: 17px;
  margin-right: 20px;
  margin-top: 10px;
  color: #ff7c2d;
}
.detail {
  width: 228px;
  height: 418px;
  border: 1px solid #a5a5a5;
  border-top: 0;
}
</style>