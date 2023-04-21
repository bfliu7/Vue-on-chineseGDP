<template>
  <Echart id="rightTop" :options="option" class="right_top_inner" v-if="pageflag" ref="charts" />
  <Reacquire v-else @onclick="get_data" style="line-height: 200px">
    重新获取
  </Reacquire>
</template>
<!-- 各个省的GDP增速 -->
<script>
import { currentGET } from "api/modules";
import { graphic } from "echarts";
import * as echarts from "echarts";

export default {
  data() {
    return {
      option: {},
      lists:{"children":[{"name":"左上","value":0},{"name":"左中","value":0},{"name":"左下","value":0},{"name":"中图","value":0},{"children":[{"name":"右上图","value":0},{"name":"右上大图","value":0}],"name":"右上"},{"children":[{"name":"右中图","value":0},{"name":"右中大图","value":0}],"name":"右中"},{"name":"右下","value":1}],"name":"各节点状态"},
      pageflag: false,
      isFullScreen: false
    };
  },
  created() { },

  beforeMount() {
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
      }
    },
    get_data() {
      this.pageflag = true;
      this.$http
        .get("/right_bottom")
        .then((response) => {
          if (this.lists == response.data) {
            console.log
          }
          else {
            this.lists = response.data;
            this.init(this.lists)
          }
          this.switper()
        })
        .catch((error) => {
          console.log(error);
        });
    },

    //轮询
    switper() {
      if (this.timer) {
        return;
      }
      let looper = (a) => {
        this.get_data();
      };
      this.timer = setInterval(looper, 10000);
    },
    
    init(xdata) {
      this.option = {
        textStyle:{
          fontSize:14,
          color:'white'
        },

        tooltip: {
          trigger: 'item',
          backgroundColor: "rgba(0,0,0,.6)",
          borderColor: "rgba(147, 235, 248, .8)",
          textStyle: {
            color: "#FFF",
            fontSize: 15,
          },
          triggerOn: 'mousemove',
          formatter:function(params){
            var str=''
            if(params.value==0){
              str += '断开'
            }
            else{
              str += '连接'
            }
            return str
          }
        },
        legend: {
          show:false,
          top: '2%',
          left: '50%',
          orient: 'vertical',
          data: [
            {
              name: 'tree1',
              icon: 'rectangle'
            },
          ],
          borderColor: '#c23531'
        },
        series: [
          {
            type: 'tree',
            name: 'tree1',
            data: [xdata],
            top: '1%',
            left: '20%',
            bottom: '5%',
            right: '20%',
            symbolSize: 7,
            label: {
              position: 'left',
              verticalAlign: 'middle',
              align: 'right'
            },
            leaves: {
              label: {
                position: 'right',
                verticalAlign: 'right',
                align: 'left'
              }
            },
            emphasis: {
              focus: 'descendant'
            },
            expandAndCollapse: true,
            animationDuration: 550,
            animationDurationUpdate: 750
          },

        ]
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.right_top_inner {
  margin: 0px;
  padding: 0px;
  border: 0px;
}
</style>
