<template>
  <el-container>
    <el-header>
      <div>
        <el-input placeholder="请输入内容" v-model="input1" class="input-with-select" style="width: 50%">
          <template slot="prepend">Name:</template>
        </el-input>
        <el-input placeholder="请输入内容" v-model="input2" class="input-with-select" style="width: 50%">
          <template slot="prepend">Tag:</template>
          <el-button slot="append" icon="el-icon-search" @click="postSearch()"></el-button>
        </el-input>
      </div>
    </el-header>
    <el-main>
      <el-table
        :data="tableData"
        style="width: 100%">
        <el-table-column
          prop="name"
          label="name"
          width="180">
        </el-table-column>
        <el-table-column
          prop="is_official"
          label="is_official"
          width="180">
        </el-table-column>
        <el-table-column
          prop="star_count"
          label="star_count">
        </el-table-column>
        <el-table-column
          prop="is_automated"
          label="is_automated">
        </el-table-column>
        <el-table-column
          prop="description"
          label="description">
        </el-table-column>
        <el-table-column
          fixed="right"
          label="action"
          width="100">
          <template slot-scope="scope">
            <el-button @click="handleClick(scope.row)" type="text" size="small">pull</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-main>
  </el-container>
</template>
<script>
import Schart from 'vue-schart';
import bus from '../common/bus';
import axios from 'axios';
export default {
  data() {
    return {
      input1: '',
      input2: '',
      tableData: []
    }
  },
  methods:{
    postSearch(){
      var that = this;
      console.log(that.input1);
      console.log(that.input2);
      let dic={
        "name":this.input1,
        "tag":this.input2
      }
      axios.post("/images/find/",dic)
      .then(function(response){
        console.log(response.data);
        that.tableData=response.data;
      });
    },
     handleClick(row) {
        console.log(row);
        let dic={
          "name":row.name
        }
        console.log(dic)
        axios.post("/images/pull/",dic)
        .then(function(response){
          alert(response.data["msg"]);
        });
    }
  }
}
</script>
<style>
  .el-header, .el-footer {
    color: #333;
    text-align: left;
    line-height: 60px;
  }
  
  .el-aside {
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    line-height: 200px;
  }
  
  .el-main {
    color: #333;
    text-align: center;
    line-height: 80px;
  }
  
  body > .el-container {
    margin-bottom: 40px;
  }
  
  .el-container:nth-child(5) .el-aside,
  .el-container:nth-child(6) .el-aside {
    line-height: 260px;
  }
  
  .el-container:nth-child(7) .el-aside {
    line-height: 320px;
  }
</style>