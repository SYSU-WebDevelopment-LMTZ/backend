webpackJsonp([5],{bkU3:function(e,t,a){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var r=a("riiq"),l=a("aozt"),n=a.n(l),s={data:function(){return{searchText:"",allorders:[],orders_map:[],merchant_id:this.merchant.merchant_id,inputDate:"",loading:!0,pages:5,startDate:"",endDate:""}},created:function(){this.getData()},components:{headtop:r.a},methods:{search:function(){this.searchText},getData:function(){var e=this;console.log("get all orders");n.a.get("http://localhost:5000/order").then(function(t){e.allorders=t.data,console.log("get all orders success"),console.log(t.data)}).catch(function(e){console.log("get all orders fail"),console.log(e)})},reArraneOrder:function(){var e=new Date(that.startDate),t=new Date(that.endDate);that.allorders.forEach(function(a){var r=new Date(a.publish_at);a.show=r>=e&&r<=t})},searchOrder:function(e){that.loading=!0,console.log(e)}}},o={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"orders"},[a("headtop",{on:{search:e.search},model:{value:e.searchText,callback:function(t){e.searchText=t},expression:"searchText"}}),e._v(" "),a("el-tag",{staticClass:"info-tag"},[e._v("\n    今日订单\n  ")]),e._v(" "),a("div",{staticClass:"orders-table"},[a("el-date-picker",{staticClass:"date-picker",attrs:{type:"daterange","range-separator":"至","start-placeholder":"开始日期","end-placeholder":"结束日期"},model:{value:e.inputDate,callback:function(t){e.inputDate=t},expression:"inputDate"}}),e._v(" "),a("el-button",{attrs:{type:"primary",icon:"el-icon-search"},on:{click:e.searchOrder}},[e._v("搜索")]),e._v(" "),a("el-table",{staticClass:"order",staticStyle:{width:"100%"},attrs:{border:"",data:e.allorders}},[a("el-table-column",{attrs:{type:"expand"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-form",{staticClass:"demo-table-expand",attrs:{"label-position":"left",inline:""}},[a("el-form-item",{attrs:{label:"桌号"}},[a("span",[e._v(e._s(t.row.tableid))])]),e._v(" "),a("el-form-item",{attrs:{label:"是否已支付"}},[a("span",[e._v(e._s(t.row.state))])]),e._v(" "),a("el-form-item",{attrs:{label:"备注"}},[a("span",[e._v(e._s(t.row.note))])]),e._v(" "),a("el-form-item",{attrs:{label:"商品"}})],1),e._v(" "),a("el-table",{attrs:{data:t.row.dishes,"header-align":"center",size:"mini",border:""}},[a("el-table-column",{attrs:{label:"菜品",prop:"dishname","header-align":"center",align:"center"}}),e._v(" "),a("el-table-column",{attrs:{label:"份数",prop:"dishcount","header-align":"center",align:"center"}})],1)]}}])}),e._v(" "),a("el-table-column",{attrs:{label:"订单号",prop:"orderid"}}),e._v(" "),a("el-table-column",{attrs:{label:"订单金额",prop:"price"}}),e._v(" "),a("el-table-column",{attrs:{label:"下单日期",prop:"ordertime"}}),e._v(" "),a("el-table-column",{attrs:{label:"订单状态",prop:"state"},scopedSlots:e._u([{key:"default",fn:function(t){return[e._v("\n          "+e._s(t.row.state)+"\n        ")]}}])})],1),e._v(" "),a("el-pagination",{staticClass:"pagination",attrs:{layout:"prev, pager, next",total:e.pages}})],1)],1)},staticRenderFns:[]};var c=a("C7Lr")(s,o,!1,function(e){a("pLGO")},null,null);t.default=c.exports},pLGO:function(e,t){}});
//# sourceMappingURL=5.b05c83ccef5f412b5693.js.map