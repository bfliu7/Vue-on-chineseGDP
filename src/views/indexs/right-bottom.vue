<!--
 * @Author: daidai
 * @Date: 2022-03-01 15:27:58
 * @LastEditors: Please set LastEditors
 * @LastEditTime: 2022-05-07 11:24:14
 * @FilePath: \web-pc\src\pages\big-screen\view\indexs\right-center.vue
-->
<template>
  <div v-if="pageflag" class="right_center_wrap beautify-scroll-def" :class="{ 'overflow-y-auto': !sbtxSwiperFlag }">
    <component :is="components" :data="list" :class-option="defaultOption">
      <ul class="right_center ">
        <li class="right_center_item" v-for="(item, i) in list" :key="i">
          <span class="orderNum">{{ i + 1 }}</span>
          <div class="inner_right">
            <div class="dibu"></div>
            <div class="flex">
              <div class="info">
                <span class="labels ">站口名称：</span>
                <span class="contents zhuyao"> {{ item.gatewayno }}</span>
              </div>
              <!-- <div class="info">
                <span class="labels">型号：</span>
                <span class="contents "> {{ item.terminalno }}</span>
              </div> -->
              <div class="info">
                <span class="labels">流量告警值：</span>
                <span class="contents warning"> {{ item.alertvalue | montionFilter }}</span>
              </div>
            </div>


            <div class="flex">

              <div class="info">
                <span class="labels"> 地址：</span>
                <span class="contents ciyao" style="font-size:12px"> {{ item.provinceName }}</span>
              </div>
              <div class="info time">
                <span class="labels">时间：</span>
                <span class="contents" style="font-size:12px"> {{ item.createtime }}</span>
              </div>

            </div>
            <div class="flex">

              <div class="info">
                <span class="labels">报警内容：</span>
                <span class="contents ciyao" :class="{ warning: item.alertdetail }"> {{ item.alertdetail || '无'
                }}</span>
              </div>
            </div>
          </div>
        </li>
      </ul>
    </component>
  </div>
  <Reacquire v-else @onclick="getData" style="line-height:200px" />

</template>

<script>
let lists=[{"alertdetail": "\u6b63\u5e38", "alertvalue": 16, "createtime": "2022-12-25 19:46:02", "gatewayno": "\u677e\u5c71\u6e56\u5357", "provinceName": "\u6df1\u5733\u5e02"}, {"alertdetail": "\u6b63\u5e38", "alertvalue": 15, "createtime": "2022-12-25 19:46:02", "gatewayno": "\u5e7f\u4e1c\u7f57\u7530\u4e3b\u7ebf\u7ad9", "provinceName": "\u6df1\u5733\u5e02"}, {"alertdetail": "\u6b63\u5e38", "alertvalue": 19, "createtime": "2022-12-25 19:46:02", "gatewayno": "\u5e7f\u4e1c\u6c34\u6717D\u7ad9", "provinceName": "\u6df1\u5733\u5e02"}];
import { currentGET } from 'api/modules'
import vueSeamlessScroll from 'vue-seamless-scroll'  // vue2引入方式
import Kong from '../../components/kong.vue'
export default {
  components: { vueSeamlessScroll, Kong },

  data() {
    return {
      list: [],
      pageflag: true,
      defaultOption: {
        ...this.$store.state.setting.defaultOption,
        limitMoveNum: 3, 
        singleHeight: 250, 
        step:0,
      }

    };
  },
  computed: {
    sbtxSwiperFlag() {
      let ssyjSwiper = this.$store.state.setting.ssyjSwiper
      if (ssyjSwiper) {
        this.components = vueSeamlessScroll
      } else {
        this.components = Kong
      }
      return ssyjSwiper
    }
  },
  created() {
    this.getData()
  },

  mounted() { },
  methods: {
    fn(){ //记得调用fn
          this.$http_alarm.get('/right-bottom')
          .then(function (response){
          lists=response.data
          // console.log(response.data)
          })
          .catch (function (error){console.log(error);});
    },
    getData() {
      // this.fn()
      this.pageflag = true
      // this.pageflag =false
      currentGET('big5', { limitNum: 50 }).then(res => {
        // if (!this.time){console.log("right-bottom", res);}
        if (res.success) {
          this.list = lists
          let timer = setTimeout(() => {
              clearTimeout(timer)
              this.defaultOption.step=this.$store.state.setting.defaultOption.step
          }, this.$store.state.setting.defaultOption.waitTime);
          this.switper();
        } else {
          this.pageflag = false
          this.$Message.warning(res.msg)
        }
      })
    },
    switper() {
            if (this.timer) {
                return
            }
            let looper = (a) => {
                this.getData()
            };
            this.timer = setInterval(looper, 5000); //10秒一换
    },

  },
};
</script>
<style lang='scss' scoped>
.right_center {
  width: 100%;
  height: 100%;

  .right_center_item {
    display: flex;
    align-items: center;
    justify-content: center;
    height: auto;
    padding: 10px;
    font-size: 14px;
    color: #fff;

    .orderNum {
      margin: 0 20px 0 -20px;
    }


    .inner_right {
      position: relative;
      height: 100%;
      width: 400px;
      flex-shrink: 0;
      line-height: 1.5;

      .dibu {
        position: absolute;
        height: 2px;
        width: 104%;
        background-image: url("../../assets/img/zuo_xuxian.png");
        bottom: -12px;
        left: -2%;
        background-size: cover;
      }
    }

    .info {
      margin-right: 10px;
      display: flex;
      align-items: center;

      .labels {
        flex-shrink: 0;
        font-size: 12px;
        color: rgba(255, 255, 255, 0.6);
      }

      .zhuyao {
        color: $primary-color;
        font-size: 15px;
      }

      .ciyao {
        color: rgba(255, 255, 255, 0.8);
      }

      .warning {
        color: #E6A23C;
        font-size: 15px;
      }
    }

  }
}

.right_center_wrap {
  overflow: hidden;
  width: 100%;
  height: 250px;
}

.overflow-y-auto {
  overflow-y: auto;
}
</style>