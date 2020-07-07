<template>
  
  <div>
    
    <Card>
      
      <h1 slot="title">Papers信息</h1>
      <Button
        type="primary"
        slot="extra"
        to="HelloWorld"
      >
        <Icon type="ios-download-outline"></Icon>回到hello页面
      </Button>
      <Table
        :columns="headers"
        :data="test_data"
        :loading='false'
        ref='table_sys_configs'
      ></Table>
      <Page :total="100" show-sizer @on-change="change" />
    </Card>
  </div>
</template>

<script>
export default {
  created () {
    var that = this
    this.$axios.get('get_data', {
      params: {
        venue: 'nips',
        page: 2
      }
    }).then(function (res) {
      that.test_data = res.data.result
      console.log(res.data)
    }).catch(function (error) {
      console.log(err)
    })
  },
  data () {
    return {
      test_data: [],
      headers: [
        {
          title: 'title',
          key: 'title',
          align: 'center'
        },
        {
          title: 'desc',
          key: 'abstract',
          align: 'center'
        },
        {
          title: '备注',
          key: '111',
          align: 'center'
        }
      ],
      element: '',
      showdata: true,
    }
  },
  methods: {
    change(data) {
      console.log(data)
      var that = this
      this.$axios.get('get_data', {
      params: {
        venue: 'NIPS',
        page: data
      }
    }).then(function (res) {
      that.test_data = res.data.result
      console.log(res.data)
    }).catch(function (error) {
      console.log(err)
    })

    }
  }
}
</script>