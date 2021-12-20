<template>
  <div>
    <Header></Header>
    <div class="w">
      <div class="box">
        <div class="pic">
          <img :src="movie.img" alt="">
        </div>
        <div class="detail">
          <h1 class="h1">{{movie.movie}}</h1>
          <p class="summary"><span>简介: {{movie.summary}}</span></p>
          <h2 class="h2">导演: {{movie.director}}</h2>
          <h2 class="h2">类型: {{movie.genre}}</h2>
          <h3 class="h3">评分: {{movie.rating}}</h3>
          <h3 class="h3">你的评价:</h3>
          <ul>
            <li><a @click="like" class="left">喜欢</a></li>
            <li><a @click="dislike" class="right">不喜欢</a></li>
          </ul>
        </div>
        <div class="rank">
          <h4>热门排行榜</h4>
          <ul>
            <li v-for="item in rankList" :key="item.id">
              <p>{{item.id}}</p><a :href="'/single?movieid='+item.movieid">{{item.name}}</a>
            </li>
          </ul>
        </div>
      </div>
      <!-- 推荐区域 -->
      <div class="box-hd">
        <h3>你可能喜欢</h3>
      </div>
      <div class="box-bd">
        <ul>
          <li v-for="item in movieList" :key="item.id">
            <a :href="'/single?movieid='+item.id" class="detail1">
              <img :src="item.img" alt="">
              <div>
                <h1>{{item.name}}</h1>
                <span class="name">{{item.director}}</span>
                <span class="rate">{{item.rate}}</span>
              </div>
            </a>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios'
export default {
  name: 'Single',
  async created() {
    var query = this.$route.query.movieid
    // 插入历史记录
    this.insertHistory(query)
    if (query) {
      axios
        .get('/api/find', {
          params: {
            movieid: query
          }
        })
        .then(res => {
          console.log(res.data.data[0])
          this.movie = res.data.data[0]
          // 排行榜
          axios.get('/api/ranklist').then(res => {
            console.log(res.data.data)
            this.rankList = res.data.data
          })
          // 寻找相似电影
        })
      let result = await axios.get('/api/similar', {
        params: {
          id: query
        }
      })
      // console.log('11',result.data.data)
      if (result.data.code == '200') {
        this.movieList = result.data.data
      }
    }
  },
  data() {
    return {
      movie: {},
      rankList: [],
      movieList: [],
      username: sessionStorage.getItem('username')
    }
  },
  methods: {
    async like() {
      if (sessionStorage.getItem('username')) {
        this.$message.success('评价成功!')
        let result = await axios({
          method: 'post',
          url: '/api/likemovie',
          data: { moviegenre: this.movie.genre, username: this.username }
        })
        // console.log(result)
      } else {
        this.$message.error('请先登录再作评价!')
        this.$router.push('/login')
      }
    },
    async dislike() {
      if (sessionStorage.getItem('username')) {
        this.$message.success('评价成功!')
        let result = await axios({
          method: 'post',
          url: '/api/dislikemovie',
          data: { moviegenre: this.movie.genre, username: this.username }
        })
      } else {
        this.$message.error('请先登录再作评价!')
        this.$router.push('/login')
      }
    },
    insertHistory(movieid) {
      // console.log(movieid,this.username)
      axios({
        method: 'post',
        url: '/api/inserthistory',
        data: { movieid: movieid, username: this.username }
      })
    }
  }
}
</script>
<style lang='less' scoped>
a {
  display: block;
  text-decoration: none;
  color: #000;
  cursor: pointer;
}
.box {
  height: 450px;
}
.pic {
  float: left;
  width: 300px;
  height: 450px;
  // background-color: pink;
}
.pic img {
  width: 300px;
  height: 450px;
}
.detail {
  float: left;
  height: 450px;
  width: 480px;
  margin-left: 20px;
  // background-color: #5a5a5a;
}
.rank {
  float: left;
  height: 450px;
  width: 400px;
  // background-color: #456751;
}
.h1 {
  color: #000;
  font-size: 26px;
  font-weight: 700;
  // padding-left: 10px;
  margin: 0 0 10px 0;
}
.summary {
  color: gray;
  font-size: 18px;
  width: 450px;
  height: 190px;
  // padding-left:  10px;
  margin: 0 0 10px 0;
  // 文字溢出隐藏
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 8;
  -webkit-box-orient: vertical;
}
.h2 {
  color: #000;
  font-size: 16px;
  margin-bottom: 10px;
}
.h3 {
  color: #d2232a;
  font-size: 24px;
  margin-bottom: 10px;
}
.detail ul li a {
  display: block;
  width: 100px;
  height: 40px;
  line-height: 40px;
  text-align: center;
  color: #fff;
  background-color: #d2232a;
  text-decoration: none;
}
.left {
  float: left;
}
.right {
  float: right;
  margin-right: 20px;
}
.rank h4 {
  height: 40px;
  line-height: 40px;
  text-align: center;
  font-size: 24px;
  margin-bottom: 10px;
  border-bottom: 1px solid #c5933d;
}

.rank ul li p {
  float: left;
  text-align: center;
  line-height: 40px;
  width: 40px;
  height: 40px;
  color: #a52a2a;
}

.rank ul li a {
  float: left;
  height: 40px;
  width: 230px;
  line-height: 40px;
  text-decoration: none;
  color: #000;
  font-size: 18px;
  margin-left: 130px;
}
.rank ul li a:hover {
  color: #a52a2a;
}

.box-hd {
  margin-top: 15px;
  margin-bottom: 15px;
}

.box-bd li {
  float: left;
  width: 230px;
  height: 420px;
  // background-color: pink;
  margin-right: 15px;
}
.box-bd li:hover {
  background-color: rgba(218, 217, 217, 0.7);
}
.box-bd li img {
  display: block;
  width: 100%;
  height: 342px;
}
.box-bd ul li a h1 {
  font-size: 18px;
  font-weight: normal;
  margin: 5px 0px 5px 10px;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
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
.detail1 {
  width: 228px;
  height: 418px;
  border: 1px solid #a5a5a5;
  border-top: 0;
}
</style>