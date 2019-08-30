<template>
  <div class="hello">
    <el-container>
      <el-header>温湿度监控平台</el-header>
      <el-main>
        <div class="main">
          <div class="figure">
            <div id="fig" class="temperature-fig">
              <v-chart ref="chart1" :options="tempOptions" :auto-resize="true"></v-chart>
              <span>温度</span>
            </div>
            <div id="fig" class="humidity-fig">
              <v-chart ref="chart1" :options="humiOptions" :auto-resize="true"></v-chart>
              <span>湿度</span>
            </div>
            <div>
              <el-table :data="tableData" style="width: 100%" max-height="300">
                <el-table-column prop="datetime" label="日期" :formatter="dateFormat" width="180">
                </el-table-column>
                <el-table-column prop="temperature" label="温度" :formatter="tempFormat" width="180">
                </el-table-column>
                <el-table-column prop="humidity" label="湿度" :formatter="humiFormat">

                </el-table-column>
              </el-table>
            </div>
          </div>

          <div class="button">
            <el-button type="primary" @click="openTimer">设置定时浇灌</el-button>
            <el-button type="primary" @click="getHistoryData">查看历史记录</el-button>
          </div>
        </div>
      </el-main>
    </el-container>
    <el-dialog title="历史数据" :visible.sync="HistoryVisible">
      <el-table :data="historyData" max-height="300">
        <el-table-column prop="datetime" label="日期" :formatter="dateFormat" width="180"></el-table-column>
        <el-table-column prop="temperature" label="温度" :formatter="tempFormat" width="180"></el-table-column>
        <el-table-column prop="humidity" label="湿度" :formatter="humiFormat"></el-table-column>
      </el-table>
    </el-dialog>
    <el-dialog title="定时浇灌" :visible.sync="TimerVisible" @close="handleClose">
      <div class="timer">
        <el-time-picker v-model="setTime"  placeholder="任意时间点"></el-time-picker>
        <el-input v-model="lightTime" placeholder="请输入浇灌时间"></el-input>
        <el-button type="primary" @click="lightLed">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
  import ECharts from 'vue-echarts'
  import 'echarts/lib/chart/pie'
  import '../assets/basic.css'
  import moment from 'moment'
  export default {
    name: 'HelloWorld',
    components: {
      'v-chart': ECharts
    },
    data() {
      return {
        tableData: [],
        historyData: [],
        tempOptions: {
          legend: {
            orient: 'vertical',
            x: 'left',
            data: ['', '', '']
          },
          series: [{
            name: '访问来源',
            type: 'pie',
            radius: ['65%', '70%'],
            hoverAnimation: false,
            avoidLabelOverlap: false,
            startAngle: 225,
            label: {
              normal: {
                show: true,
                position: 'center',
                fontSize: 32,
              },
            },
            labelLine: {
              normal: {
                show: false
              }
            },
            data: [{
                value: 90,
                name: '27°C',
                itemStyle: {
                  color: {
                    type: 'linear',
                    x: 0,
                    y: 0,
                    x2: 0,
                    y2: 1,
                    colorStops: [{
                        offset: 0,
                        color: 'rgba(255,127,80,1)' // 0% 处的颜色
                      },
                      {
                        offset: 1,
                        color: 'rgba(255,0,0,1)' // 100% 处的颜色
                      }
                    ],
                    global: false // 缺省为 false
                  },
                },
              },
              {
                value: 180,
                name: '',
                itemStyle: {
                  color: '#eeeeee'
                }
              },
              {
                value: 90,
                name: '',
                itemStyle: {
                  color: '#FFFFFF'
                }
              }
            ],
            animation: false,
          }]
        },
        humiOptions: {
          legend: {
            orient: 'vertical',
            x: 'left',
            data: ['', '', '']
          },
          series: [{
            name: '访问来源',
            type: 'pie',
            radius: ['65%', '70%'],
            hoverAnimation: false,
            avoidLabelOverlap: false,
            startAngle: 225,
            label: {
              normal: {
                show: true,
                position: 'center',
                fontSize: 32,
              },
              // emphasis: {
              //   show: true,
              //   textStyle: {
              //     fontSize: '30',
              //     fontWeight: 'bold'
              //   }
              // }
            },
            labelLine: {
              normal: {
                show: false
              }
            },
            data: [{
                value: 90,
                name: '80%',
                itemStyle: {
                  color: {
                    type: 'linear',
                    x: 0,
                    y: 0,
                    x2: 0,
                    y2: 1,
                    colorStops: [{
                        offset: 0,
                        color: 'rgba(103,222,255,1)' // 0% 处的颜色
                      },
                      {
                        offset: 1,
                        color: 'rgba(64,158,255,1)' // 100% 处的颜色
                      }
                    ],
                    global: false // 缺省为 false
                  },
                },
              },
              {
                value: 180,
                name: '',
                itemStyle: {
                  color: '#eeeeee'
                }
              },
              {
                value: 90,
                name: '',
                itemStyle: {
                  color: '#FFFFFF'
                }
              }
            ],
            animation: false,
          }]
        },
        obj: null,
        timer: null,
        setTime:'',
        lightTime: '',
        HistoryVisible: false,
        TimerVisible: false
      }
    },
    watch: {
      'obj': function(obj){
        if(obj.temperature>37){
          this.$notify({
            title: '警告',
            message: '温度过高！',
            type: 'warning'
          });
        };
        if(obj.humidity>70){
          this.$notify({
            title: '警告',
            message: '湿度过高！',
            type: 'warning'
          });
        }
      }
    },
    methods: {
      async getData() {
        let res = await this.$http.get('http://172.20.10.4:5000/getData');
        this.obj=res.body;
        // this.obj.data=this.obj.data*1000;
        this.tableData.unshift(res.body);
        
        this.tempOptions.series[0].data[0].value = res.body.temperature * 2.7;
        this.tempOptions.series[0].data[0].name = res.body.temperature + '°C';
        this.tempOptions.series[0].data[1].value = (100 - res.body.temperature) * 2.7;
        this.humiOptions.series[0].data[0].value = res.body.humidity * 2.7;
        this.humiOptions.series[0].data[0].name = res.body.humidity + '%';
        this.humiOptions.series[0].data[1].value = (100 - res.body.humidity) * 2.7;
      },
      async lightLed() {
        let now = new Date().getTime()
        let setTime = this.setTime.getTime();
        let sleepTime = (setTime-now)/1000;
        let lightTime = this.lightTime;
        await this.$http.get(`http://172.20.10.4:5000/lightLed?sleepTime=${sleepTime}&lightTime=${lightTime}`).then(res => {
            this.$message({
              message: '成功发送浇灌信息',
              type: 'success'
            });
            this.lightTime = '';
          },
          err => {
            this.$message.error('发送浇灌信息失败,请再次尝试');
          });
      },
      async getHistoryData() {
        this.HistoryVisible = true;
        let res = await this.$http.get('http://172.20.10.4:5000/getHistory');
        console.log(res);
        this.historyData = res.body;
      },
      dateFormat(row, column) {
        return moment(row[column.property] * 1000).format('YYYY-MM-DD hh:mm:ss');
      },
      tempFormat(row, column, cellValue, index) {
        return cellValue + '°C';
      },
      humiFormat(row, column, cellValue, index) {
        return cellValue + '%';
      },
      openTimer(){
        this.TimerVisible=true;
        this.setTime=new Date();
      },
      handleClose() {
        this.lightTime = '';
        this.setTime='';
      }
    },
    created() {
      // this.getData();
      // console.log(this.tableData);
      this.timer = setInterval(this.getData, 5000);
    },
    beforeDestroy() {
      clearInterval(this.timer);
    },
  }

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="less" scoped>
  .echarts {
    width: 100%;
    height: 100%;
  }

  .figure {
    display: flex;
    justify-content: space-between;

    #fig {
      position: relative;
      width: 32%;
      height: 300px;
      border: 1px solid #dddddd;

      span {
        display: inline-block;
        position: absolute;
        width: 50px;
        text-align: center;
        top: 70%;
        left: 45%;
        font-size: 25px;
      }
    }
  }

  .button {
    padding-top: 10px;
    display: flex;
    justify-content: center;
  }

  .timer {
    display: flex;
    justify-content: flex-start;
  }

</style>
