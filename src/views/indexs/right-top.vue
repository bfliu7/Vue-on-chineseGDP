<template>
  <Echart
    id="rightTop"
    :options="option"
    class="right_top_inner"
    v-if="pageflag"
    ref="charts"
  />
  <Reacquire v-else @onclick="getData" style="line-height: 200px">
    重新获取
  </Reacquire>
</template>

<script>
import * as echarts from "echarts";
import "echarts-gl";

export default {
  data() {
    return {
      option: {},
      lists: [
              ["安徽", 8.04],
              ["四川", 6.95],
            ],
      pageflag: false,
      timer: null,
      symbolSize: 2.5,
    };
  },
  created() {},

  beforeMount(){
    this.init(this.lists);
  },
  mounted() {
    this.get_data();
  },
  beforeDestroy() {
    this.clearData();
  },
  methods: {
    clearData() {
      if (this.timer) {
        clearInterval(this.timer);
        this.timer = null;
      }
    },
    get_data() {
      this.pageflag = true;
      this.$http
        .get("/right_top")
        .then((response) => {
          this.lists = response.data;
          this.init(this.lists)
        })
        .catch((error) => {
          console.log(error);
        });
    },
    handleFull(){
      console.log
    },
    //轮询
    switper() {
      if (this.timer) {
        return;
      }
      let looper = (a) => {
        this.get_data();
      };
      this.timer = setInterval(looper, 1000);
    },
    init(xdata) {
      this.option = {
        xAxis: {
          type: "category",
        },
        yAxis: {},
        tooltip: {},
        series: [
          {
            symbolSize: 20,
            data: xdata,
            type: "scatter",
          },
        ],
        toolbox: {
          feature: {
            myFull: {
              // 自定义全屏按钮
              show: true,
              title: "全屏",
              icon: "path://M432.45,595.444c0,2.177-4.661,6.82-11.305,6.82c-6.475,0-11.306-4.567-11.306-6.82s4.852-6.812,11.306-6.812C427.841,588.632,432.452,593.191,432.45,595.444L432.45,595.444z M421.155,589.876c-3.009,0-5.448,2.495-5.448,5.572s2.439,5.572,5.448,5.572c3.01,0,5.449-2.495,5.449-5.572C426.604,592.371,424.165,589.876,421.155,589.876L421.155,589.876z M421.146,591.891c-1.916,0-3.47,1.589-3.47,3.549c0,1.959,1.554,3.548,3.47,3.548s3.469-1.589,3.469-3.548C424.614,593.479,423.062,591.891,421.146,591.891L421.146,591.891zM421.146,591.891", // 省略部分代码，可自行选择或设计图标
              onclick: this.handleFull, // 全屏按钮点击事件
            },
          },
        },
      };
    },
  },
};
</script>
<style lang="scss" scoped>
.right_top_inner {
  margin-top: -8px;
}
</style>
