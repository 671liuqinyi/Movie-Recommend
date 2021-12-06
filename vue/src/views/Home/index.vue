<template>
  <div>
    <Header></Header>
    <!-- 用户可能喜欢推荐 -->
    <div class="banner">
      <div class="w">
        <div class="movie">
          <img :src="this.movie.src" alt="">
        </div>
        <div class="moviedetail">
          <h3 class="moviename">《{{this.movie.name}}》</h3>
          <h3 class="comment">观众热评:</h3>
          <ul class="usercomment">
            <li v-for="(comment,index) in comments" :key="index">
              <h3>{{comment.name}}</h3>
              <p class="content">{{comment.comment}}</p>
            </li>
            <div class="btn">
              <li><a class="leftbtn" @click="checkMovieDetail">查看详情</a></li>
              <li><a class="rightbtn" @click="changeMovie">换一部</a></li>
            </div>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios'
export default {
  name: 'Home',
  inject:['routerRefresh'],
  created(){
		// console.log(this.id)
		axios.get('/api/homemovie',{
			params:{id:this.id}
		}).then(res=>{
			// console.log(res.data.data)
			this.comments = res.data.data
			this.movie.id=this.comments[0].id
			this.movie.src=this.comments[0].img
			this.movie.name=this.comments[0].moviename
		})
	},
	data(){
		return {
			id:1291554+Math.floor(Math.random()*30),
			// id:1291554,
			movie:{id:'',src:'',name:''},
			comments:[]
		}
	},
  methods:{
    changeMovie(){
			this.routerRefresh()
		},
		checkMovieDetail(){
			this.$router.push({path:'/single',query: {movieid:this.id}})
		}
  }
}
</script>
<style scoped>
.banner {
  height: 500px;
  background-color: #1a1a1a;
}
.banner .w {
  height: 500px;
  width: 1120px;
  background-color: aquamarine;
}
.banner .w .movie {
  float: left;
}
.banner .w .movie img {
  height: 500px;
  width: 368px;
}
.banner .w .moviedetail {
  float: left;
  width: 752px;
  height: 500px;
  background-color: #1a1a1a;
  color: #cbcbcb;
}
.moviename {
  height: 60px;
  text-align: center;
  line-height: 60px;
}
.comment {
  margin-bottom: 20px;
  margin-left: 100px;
}
.banner .w .moviedetail ul {
  margin-left: 100px;
}
.usercomment li h3 {
  color: #808080;
  font-size: 25px;
}
.btn a {
  height: 50px;
  width: 120px;
  color: #ffffff;
  background-color: #d2232a;
  text-decoration: none;
  font-size: 18px;
  line-height: 50px;
  text-align: center;
  cursor: pointer;
}
.btn a:hover {
  background-color: #1a7daa;
}
.leftbtn {
  float: left;
}
.rightbtn {
  float: right;
}
.content {
  height: 30px;
  padding: 6px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  border-bottom: 1px solid #808080;
  margin-bottom: 8px;

}
.lastcontent {
  border: 0;
}
</style>
