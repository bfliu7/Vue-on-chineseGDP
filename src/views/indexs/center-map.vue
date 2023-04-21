<!--
 * @Author: daidai
 * @Date: 2022-03-01 11:17:39
 * @LastEditors: Please set LastEditors
 * @LastEditTime: 2022-09-29 15:50:18
 * @FilePath: \web-pc\src\pages\big-screen\view\indexs\center-map.vue
-->

<template>
  <div style="background:transparent;height:100vh;">

    <div ref="chinaMap"
      style="width: 100%; height: 100%;border:0px solid blue;margin:0px auto;position:relative;z-index:1;margin-top: 10px;background-color: transparent!important;">
    </div>

  </div>
</template>


<script>
import * as echarts from 'echarts';
import 'echarts-gl';
import { currentGET } from "api/modules";
import { GETNOBASE } from "api";
import xzqCode from "../../utils/map/xzqCode";
import data from '../../utils/map/china.json';
export default {
  data() {
    return {
      lists: [{ "name": "安徽省", "value": "22.88" }, { "name": "北京市", "value": "7.88" }, { "name": "福建省", "value": "12.73" }, { "name": "甘肃省", "value": "13.32" }, { "name": "广东省", "value": "29.52" }, { "name": "广西壮族自治区", "value": "12.81" }, { "name": "贵州省", "value": "8.55" }, { "name": "河北省", "value": "40.49" }, { "name": "河南省", "value": "36.09" }, { "name": "黑龙江省", "value": "26" }, { "name": "湖北省", "value": "24.51" }, { "name": "湖南省", "value": "27.81" }, { "name": "吉林省", "value": "16.55" }, { "name": "江苏省", "value": "48.41" }, { "name": "江西省", "value": "18.86" }, { "name": "辽宁省", "value": "41.38" }, { "name": "内蒙古自治区", "value": "12.16" }, { "name": "宁夏回族自治区", "value": "1.73" }, { "name": "青海省", "value": "1.63" }, { "name": "山东省", "value": "43.41" }, { "name": "山西省", "value": "16" }, { "name": "陕西省", "value": "12.85" }, { "name": "上海市", "value": "36.66" }, { "name": "四川省", "value": "31.69" }, { "name": "天津市", "value": "12.8" }, { "name": "新疆维吾尔自治区", "value": "7.91" }, { "name": "云南省", "value": "11.78" }, { "name": "浙江省", "value": "24.53" }],
      options: {},
      code: "china", //china 代表中国 其他地市是行政编码
      echartBindClick: false,
      isSouthChinaSea: false, //是否要展示南海群岛  修改此值请刷新页面
    }
  },

  beforeMount() {
    this.$http.get('/center_map')
      .then((response) => {
        this.lists = response.data.list
        this.getGeojson(this.code, this.lists)
      })
      .catch((error) => { console.log(error); this.getGeojson(this.code, this.lists) });

  },

  mounted() {
    this.get_data();
  },

  methods: {

    async getGeojson(name, mydata) {
      //如果要展示南海群岛并且展示的是中国的话
      let geoname = name
      if (this.isSouthChinaSea && name == "china") {
        geoname = "chinaNanhai";
      }
      echarts.registerMap(name, data); // 注册矢量地图数据

      //如果有注册地图的话就不用再注册 了
      let mapjson = echarts.getMap(name);
      if (mapjson) {
        mapjson = mapjson.geoJSON;
      } else {
        mapjson = await GETNOBASE(`./map-geojson/${geoname}.json`).then((res) => {
          return res;
        });
        echarts.registerMap(name, mapjson);
      }
      let cityCenter = {};
      let arr = mapjson.features;
      //根据geojson获取省份中心点
      arr.map((item) => {
        cityCenter[item.properties.name] =
          item.properties.centroid || item.properties.center;
      });
      let newData = [];
      mydata.map((item) => {
        if (cityCenter[item.name]) {
          newData.push({
            name: item.name,
            value: cityCenter[item.name].concat(item.value),
          });
        }
      });
      this.initMap(name, newData);
    },

    get_data() { //记得调用fn
      this.$http.get('/center_map')
        .then((response) => {
          // console.log('rrrrrrrrr',response.data[0].value)
          // console.log(this.lists)
          // console.log('rrrrrrrr',this.lists[0].value)
          if (this.lists[0].value == response.data.list[0].value) {
            console.log
          }
          else {
            this.lists = response.data.list
            this.getGeojson(this.code, this.lists)
          }
          this.switper()
        })
        .catch(function (error) { console.log(error); });

    },

    switper() {
      if (this.timer) {
        return
      }
      let looper = (a) => {
        // console.log(11111111111,lists)
        this.get_data()
      };
      this.timer = setInterval(looper, 1000); //1秒刷新一次
    },


    initMap(name, datex) {
      let top = 45;
      let zoom = 1.05;
      let map = echarts.init(this.$refs.chinaMap);

      let option = {
        backgroundColor: "rgba(0,0,0,0)",
        tooltip: {
          show: true,
          formatter: function (params) {
            if (params.data) {
              return params.name + "：" + params.data["value"][2] + "亿元";
            } else {
              return params.name;
            }
          },
          backgroundColor: "rgba(0,0,0,.6)",
          borderColor: "rgba(147, 235, 248, .8)",
          textStyle: {
            color: "#FFF",
          },
        },
        legend: {
          show: false,
        },

        grid: {
          y: 200,
          x: 100,
        },
        visualMap: [
          {
            type: 'continuous',
            textStyle: {
              color: "#fff",
            },
            seriesIndex: 0,
            text: ['GDP'],
            left: 20,
            bottom: 20,
            calculable: true,
            max: 70000,
            inRange: {
              color: [
                'rgba(255, 230, 230,0.7)',
                'rgba(255, 205, 205,0.7)',
                'rgba(255, 178, 178,0.7)',
                'rgba(255, 153, 153,0.7)',
                'rgba(255, 128, 128,0.7)',
                'rgba(255, 102, 102,0.7)',
                'rgba(255, 77, 77,0.7)',
                'rgba(255, 51, 51,0.7)',
                'rgba(255, 25, 25,0.7)',
                'rgba(255, 0, 0,0.7)',

              ],
            },
          },
        ],
        geo3D: {
          map: 'china',
          roam: false,
          silent: false,
          selectedMode: false,

          itemStyle: {
            color: 'rgba(94,168,207, .2)',
            // opacity: 1,

            borderColor: "rgba(147, 235, 248, .8)",
            borderWidth: 1,
            areaColor: {
              type: "radial",
              x: 0.5,
              y: 0.5,
              r: 0.8,
              colorStops: [
                {
                  offset: 0,
                  color: "rgba(147, 235, 248, 0)", // 0% 处的颜色
                },
                {
                  offset: 2,
                  color: "rgba(147, 235, 248, .5)", // 100% 处的颜色
                },
              ],
              globalCoord: false, // 缺为 false
            },
            shadowColor: "rgba(128, 217, 248, .7)",
            shadowOffsetX: -2,
            shadowOffsetY: 2,
            shadowBlur: 10,
          },
          viewControl: {
            animationDurationUpdate: 20,
            distance: 120,
            beta: 0, //x轴旋转
            alpha: 55, //Y轴旋转
            panMouseButton: 'center', //平移操作使用的鼠标按键
            rotateMouseButton: 'left', //旋转操作使用的鼠标按键
          },

          label: {
            show: true,
            textStyle: {
              color: '#f90', //地图初始化区域字体颜色
              fontSize: 13,
              opacity: 1,
              backgroundColor: '#f90',
            },
          },
          emphasis: {
            //当鼠标放上去  地区区域是否显示名称
            label: {
              show: true,
              textStyle: {
                fontSize: 12,
                color: 'red',
              },

            },
          },
          light: {
            //光照阴影
            main: {
              color: '#fff', //光照颜色
              intensity: 0.9, //光照强度
              shadowQuality: 'high', //阴影亮度
              shadow: true, //是否显示阴影
              alpha: 55,
              beta: 55,
            },
            ambient: {
              intensity: 0.3,
            },
          },
        },
        series: [
          {
            name: 'bar3D',
            type: 'bar3D',
            coordinateSystem: 'geo3D',
            barSize: 1.1, //柱子粗细
            shading: 'lambert',
            opacity: 1,
            color: 'rgba(94,168,207,1)',

            bevelSize: 0,
            label: {
              show: true,
              formatter: function (params) {
                if (params.data) {
                  if (params.name == '宁夏回族自治区') { return "宁夏"; }
                  if (params.name == '广西壮族自治区') { return "广西"; }
                  if (params.name == '新疆维吾尔自治区') { return "新疆"; }
                  if (params.name == '西藏自治区') { return "西藏"; }
                  if (params.name == '内蒙古自治区') { return "内蒙古"; }
                  if (params.name == '黑龙江省') { return "黑龙江"; }
                  return params.name.substring(0, 2);
                } else {
                  return params.name;
                }
              },
              color: 'rgba(255,255,255,2)',
              fontSize: 18,
              // font

            },

            data: datex
          },


        ],
      };
      map.setOption(option, true);
    },
  },
};
</script>

<style lang="scss" scoped>
.centermap {
  margin-bottom: 120px;

  .maptitle {
    height: 110px;
    display: flex;
    justify-content: center;
    padding-top: 30px;
    box-sizing: border-box;

    .titletext {
      font-size: 28px;
      font-weight: 900;
      letter-spacing: 6px;
      background: linear-gradient(92deg,
          #0072ff 0%,
          #00eaff 48.8525390625%,
          #01aaff 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin: 0 10px;
    }

    .zuo,
    .you {
      background-size: 100% 100%;
      width: 29px;
      height: 20px;
      margin-top: 8px;
    }

    .zuo {
      background: url("../../assets/img/xiezuo.png") no-repeat;
    }

    .you {
      background: url("../../assets/img/xieyou.png") no-repeat;
    }
  }

  .mapwrap {
    height: 548px;
    width: 100%;
    // padding: 0 0 10px 0;
    box-sizing: border-box;
    position: relative;

    .quanguo {
      position: absolute;
      right: 20px;
      top: -46px;
      width: 80px;
      height: 28px;
      border: 1px solid #00eded;
      border-radius: 10px;
      color: #00f7f6;
      text-align: center;
      line-height: 26px;
      letter-spacing: 6px;
      cursor: pointer;
      box-shadow: 0 2px 4px rgba(0, 237, 237, 0.5),
        0 0 6px rgba(0, 237, 237, 0.4);
    }
  }
}
</style>
