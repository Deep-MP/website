import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import test from '@/components/test'
import nips from '@/components/nips'
import search from '@/components/search'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/test_data',
      name: 'test',
      component: test
    },
    {
      path: '/nips',
      name: 'nips',
      component: nips
    },
    {
      path: '/search',
      name: 'search',
      component: search
    }
  ]
})
