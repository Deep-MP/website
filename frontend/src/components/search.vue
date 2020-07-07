<template>
  <div>
    <Card>
      <h1>Search Github Informations</h1>
      <Input v-model="value" placeholder="Enter Paper Title" style="width: 500px" />
      <button @click="search_github">submit</button>
    </Card>
    <Card>
      <h1 slot="title">Result</h1>
      <Table height="700" :columns="headers" :data="test_data" ></Table>
    </Card>
  </div>
</template>

<script>
export default {
  data () {
    //console.log(this.data.value1)
    return {
      value: '',
      test_data: [],
      headers: [
        {
          title: 'address',
          key: 'address',
          align: 'center'
        },
        {
          title: 'frame',
          key: 'frame',
          align: 'center'
        },
        {
          title: 'size',
          key: 'size',
          align: 'center',
          sortable: true
        },
        {
          title: 'star',
          key: 'star',
          align: 'center',
          sortable: true
        },
        {
          title: 'watch',
          key: 'watch',
          align: 'center'
        },
        {
          title: 'fork',
          key: 'fork',
          align: 'center',
          sortable: true
        },
        {
          title: 'language',
          key: 'language',
          align: 'center'
        },
        {
          title: 'created',
          key: 'created_at',
          align: 'center',
        },
        {
          title: 'updated',
          key: 'updated_at',
          align: 'center'
        }
      ],
    }
  },
  methods: {
    search_github() {
      console.log("submit")
      var that = this
      this.$axios.get('get_code', {
        params: {
          title: that.value,
        }
      }).then(function (res) {
        that.test_data = res.data.result
        console.log(res.data)
      }).catch(function (error) {
        console.log(err)
      })
    },
  }
}
</script>