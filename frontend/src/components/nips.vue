<template>
  <div>
    <Card>
      <h1 slot="title">Papers</h1>
      <Dropdown trigger="click" slot="extra" transfer="true">
        <a href="javascript:void(0)">
            venue
            <Icon type="ios-arrow-down"></Icon>
        </a>
        <DropdownMenu slot="list">
            <DropdownItem>nips</DropdownItem>
            <DropdownItem>cvpr</DropdownItem>
            <DropdownItem>icml</DropdownItem>
            <DropdownItem>ieee</DropdownItem>
            <DropdownItem>arxiv</DropdownItem>
        </DropdownMenu>
    </Dropdown>
      <Table height="700" :columns="headers" :data="test_data" ></Table>
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
        page: 0
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
          title: 'authors',
          key: 'authors',
          align: 'center'
        },
        {
          title: 'abstract',
          key: 'abstract',
          align: 'center',
          tooltip: true
        },
        {
          title: 'year',
          key: 'year',
          align: 'center',
          sortable: true
        },
        {
          title: 'venue',
          key: 'venue',
          align: 'center'
        },
        {
          title: 'citations',
          key: 'citations',
          align: 'center',
          sortable: true
        },
        {
          title: 'influence',
          key: 'influence',
          align: 'center'
        },
        {
          title: 'topic',
          key: 'topic',
          align: 'center',
          tooltip: true
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
    },
    get_nips() {
      var that = this
      this.$axios.get('get_data', {
        params: {
          venue: 'nips',
        }
      }).then(function (res) {
        that.test_data = res.data.result
        console.log(res.data)
      }).catch(function (error) {
        console.log(err)
      })
    },
    get_cvpr() {
      var that = this
      this.$axios.get('get_data', {
        params: {
          venue: 'cvpr',
        }
      }).then(function (res) {
        that.test_data = res.data.result
        console.log(res.data)
      }).catch(function (error) {
        console.log(err)
      })
    },
    get_icml() {
      var that = this
      this.$axios.get('get_data', {
        params: {
          venue: 'icml',
          page: data
        }
      }).then(function (res) {
        that.test_data = res.data.result
        console.log(res.data)
      }).catch(function (error) {
        console.log(err)
      })
    },
    get_arxiv() {
      var that = this
      this.$axios.get('get_data', {
        params: {
          venue: 'arxiv',
          page: data
        }
      }).then(function (res) {
        that.test_data = res.data.result
        console.log(res.data)
      }).catch(function (error) {
        console.log(err)
      })
    },
    get_ieee() {
      var that = this
      this.$axios.get('get_data', {
        params: {
          venue: 'ieee',
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