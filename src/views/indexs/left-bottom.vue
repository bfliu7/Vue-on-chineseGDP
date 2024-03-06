<!--
 * @Author: daidai
 * @Date: 2022-03-01 15:51:43
 * @LastEditors: Please set LastEditors
 * @LastEditTime: 2022-09-29 15:12:46
 * @FilePath: \web-pc\src\pages\big-screen\view\indexs\right-bottom.vue
-->
<template>
  <div class="right_bottom">
    <dv-capsule-chart :config="config" style="width:100%;height:260px" />
  </div>
</template>

<script>


export default {

  data() {
    return {
      lists: [{ "name": "安徽省", "value": "22.88" }, { "name": "北京市", "value": "7.88" }, { "name": "福建省", "value": "12.73" }, { "name": "甘肃省", "value": "13.32" }, { "name": "广东省", "value": "29.52" }, { "name": "广西壮族自治区", "value": "12.81" }, { "name": "贵州省", "value": "8.55" }, { "name": "河北省", "value": "40.49" }, { "name": "河南省", "value": "36.09" }, { "name": "黑龙江省", "value": "26" }, { "name": "湖北省", "value": "24.51" }, { "name": "湖南省", "value": "27.81" }, { "name": "吉林省", "value": "16.55" }, { "name": "江苏省", "value": "48.41" }, { "name": "江西省", "value": "18.86" }, { "name": "辽宁省", "value": "41.38" }, { "name": "内蒙古自治区", "value": "12.16" }, { "name": "宁夏回族自治区", "value": "1.73" }, { "name": "青海省", "value": "1.63" }, { "name": "山东省", "value": "43.41" }, { "name": "山西省", "value": "16" }, { "name": "陕西省", "value": "12.85" }, { "name": "上海市", "value": "36.66" }, { "name": "四川省", "value": "31.69" }, { "name": "天津市", "value": "12.8" }, { "name": "新疆维吾尔自治区", "value": "7.91" }, { "name": "云南省", "value": "11.78" }, { "name": "浙江省", "value": "24.53" }],
      gatewayno: '',
      config: {
        showValue: true,
        unit: "亿",
        data: []
      },

    };
  },

  beforeMount() {
    this.config = {
              ...this.config,
              data: this.mysort(this.lists)
            }
  },

  mounted() {
    this.get_data()
  },
  beforeDestroy() {
    this.clearData()
  },
  methods: {
    get_data() { //记得调用fn
      this.pageflag = true
      this.$http.get('/left_bottom')
        .then((response) => {
          if (this.lists[0].value == response.data[0].value) {
            console.log
          }
          else {
            this.lists = response.data
            this.config = {
              ...this.config,
              data: this.mysort(this.lists)
            }
          }
          this.switper()
        })
        .catch((error) => {
          console.log(error);
          this.config = {
            ...this.config,
            data: this.mysort(this.lists)
          }
        });
    },

  
    clearData() {
      if (this.timer) {
        clearInterval(this.timer)
        this.timer = null
      }
    },
    //轮询
    switper() {
      if (this.timer) {
        return
      }
      let looper = (a) => {
        this.get_data()
      };
      this.timer = setInterval(looper, 1000);//this.$store.state.setting.echartsAutoTime
    },

    mysort(list) {
      let newNum = [], numObj = {}
      list.map(item => {
        if (!numObj[item.name] && newNum.length < 32) {
          numObj[item.name] = true
          newNum.push(item)
        }
      })
      let arr = newNum.sort((a, b) => {
        return b.value - a.value
      })
      // console.log(arr)
      let brr = []
      for (let i = 0; i < 8; i++) {
        brr.push(arr[i])
        // console.log(1111,arr[i])
      }
      // console.log(brr)

      return brr
    }


  },
};
</script>
<style lang='scss' scoped>
.list_Wrap {
  height: 100%;
  overflow: hidden;

  :deep(.kong) {
    width: auto;
  }
}

.sbtxSwiperclass {
  .img_wrap {
    overflow-x: auto;
  }

}

.right_bottom {
  box-sizing: border-box;
  padding: 0 16px;

  .searchform {
    height: 80px;
    display: flex;
    align-items: center;
    justify-content: center;

    .searchform_item {
      display: flex;
      justify-content: center;
      align-items: center;

      label {
        margin-right: 10px;
        color: rgba(255, 255, 255, 0.8);
      }

      button {
        margin-left: 30px;
      }

      input {}
    }
  }

  .img_wrap {
    display: flex;
    // justify-content: space-around;
    box-sizing: border-box;
    padding: 0 0 20px;
    // overflow-x: auto;

    li {
      width: 105px;
      height: 137px;
      border-radius: 6px;
      overflow: hidden;
      cursor: pointer;
      // background: #84ccc9;
      // border: 1px solid #ffffff;
      overflow: hidden;
      flex-shrink: 0;
      margin: 0 10px;

      img {
        flex-shrink: 0;
      }
    }




  }

  .noData {
    width: 100%;
    line-height: 100px;
    text-align: center;
    color: rgb(129, 128, 128);
  }
}
</style>
