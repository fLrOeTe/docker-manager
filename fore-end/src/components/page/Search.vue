<template>
  <div class="block">
    组织：
    <div style="margin: 5px 0;"></div>
    <el-col :span="4">
        <el-input v-model="org" placeholder="请输入内容"></el-input>
    </el-col>
    <br>
    <br>
    <span class="demonstration">时间：</span>
    <div style="margin: 5px 0;"></div>
    <el-date-picker
    v-model="value1"
    type="date"
    placeholder="选择日期">
    </el-date-picker>
    <el-button slot="append" icon="el-icon-search" @click="finddata"></el-button>
    <div style="margin: 50px 0;"></div>
    <el-table
            :data="info"
            border
            style="width: 80%">
            <el-table-column
            fixed
            prop="url"
            label="网址"
            width="200">
            </el-table-column>
            <el-table-column
            prop="org"
            label="组织"
            width="200">
            </el-table-column>
            <el-table-column
            prop="time"
            label="时间"
            width="200">
            </el-table-column>
            <el-table-column
            prop="status"
            label="状态"
            width="200">
            </el-table-column>
            <el-table-column
            fixed="right"
            label="操作"
            width="100">
                <template slot-scope="scope">
                    <el-button @click="handleClick(scope.row)" type="text" size="small">查看</el-button>
                </template>
            </el-table-column>
        </el-table>
  </div>

</template>

<script>
  import Schart from 'vue-schart';
  import bus from '../common/bus';
  import axios from 'axios';
  function checkTime(i){
        if(i<10){
          i = '0'+i
        }
        return i
  }
  function stripscript(s)
  {
    var pattern = new RegExp("[`~!@#$^&*()=|{}':;',\\[\\]<>/?~！@#￥……&*（）——|{}【】‘；：”“'。，、？]")
    var rs = "";
    for (var i = 0; i < s.length; i++) {
      rs = rs+s.substr(i, 1).replace(pattern, '');
    }
    return rs;
  } 
    export default {
    name:"search",
    data() {
      return {
        info:[{
                    url:"",
                    time:"",
                    status:"",
                    org:"",
                }],
        org:"",
        value1:"",
        pickerOptions: {
          disabledDate(time) {
            return time.getTime() > Date.now();
          },
          shortcuts: [{
            text: '今天',
            onClick(picker) {
              picker.$emit('pick', new Date());
            }
          }, {
            text: '昨天',
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() - 3600 * 1000 * 24);
              picker.$emit('pick', date);
            }
          }, {
            text: '一周前',
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit('pick', date);
            }
          }]
        },
      };
    },
     methods: {
      handleClick(row) {
              console.log(row);
              //var strs="url:"+row.url+"<br>"+"org:"+row.org+"<br>"
              var strs="<h1>Info:</h1><table border=\"1\"><tr><td><b>url</b></td><td>"+row.url+"</td></tr><tr><td><b>org</b></td><td>"+row.org+"</td></tr><tr><td><b>time</b></td><td>"+row.time+"</td></tr><tr><td><b>status</b></td><td>"+row.status+"</td></tr></table>"
              this.$alert(strs, {
                confirmButtonText: '确定',
                callback: action => {
                    this.$message({
                    type: 'info',
                    message: `action: ${ action }`
                    });
                },
                dangerouslyUseHTMLString: true,
                });
          },
      deleteRow(index, rows) {
        rows.splice(index, 1);
      },
      finddata(){
        var data=new Date("month/dd/yyyy hh:mm:ss");
        var time=this.value1;
        var date; date= new Date(time)
        var dateTime = date.getFullYear()+'/'+checkTime(date.getMonth()+1)+'/'+checkTime(date.getDate()); console.log(dateTime)
        var that=this;
        var org=stripscript(this.org);
        let para = {
          "org":org,
          "time":dateTime,
        }
        console.log(data);
        axios
        .request({
          url:"/api/testfind/",
          method:"POST",
          data:para,
        }).then(function(response){
          that.info=response.data
        });
      },
    },
    created(){
            var that = this;
            axios("/api/gettest/")
            .then(function(response){
                console.log(response.data)
                that.info=response.data
            });
        },
  };
</script>