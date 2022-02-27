import Vue from 'vue'
import Router from 'vue-router'
import ScheduleRouter from '@/components/Schedule/Schedule-router'
import FrontPageRouter from '@/components/FrontPage/FrontPage-router'
import ItineraryRouter from '@/components/Itinerary/Itinerary-router'
import PageNotFoundRouter from '@/components/Utils/PageNotFound-router'
import ItineraryTabItem from '@/components/Itinerary/ItineraryTabItem'

import axios from 'axios'

let firstVisit = true;

FrontPageRouter.beforeRouteLeave = function (to, from, next) {
    if (firstVisit && (to.name == 'schedule' && to.params.location === undefined)) { // users do not provide any location on the first visit
        this.$refs.textField.showErrorMessage();
        return false;
    } else {
        next();
    }
}

ItineraryRouter.beforeRouteEnter = function (to, from, next) {
    const access_token = Vue.cookie.get('access_token')

    if (access_token === null) {
        next(vm => {
            const ItineraryTabs = vm.$refs.ItineraryTabs;

            ItineraryTabs.overlay = true;

        });
        // user doesn't have access token, redirect to login
        // next("/404")
        // next(vm => {
        //     const app = vm.$root.$children[0]
        //     app.handleClickSignIn(function () {

        //         const cookie = Vue.cookie.get('access_token')

        //         if (cookie !== null) {
        //             const headers = {
        //                 "Content-Type": "application/json",
        //                 Authorization: "Bearer " + cookie,
        //             };

        //             axios
        //                 .get("http://127.0.0.1:8000/trip/itinerary/", {
        //                     headers,
        //                 })
        //                 .then((resp) => {
        //                     const ItineraryTabs = vm.$refs.ItineraryTabs;
        //                     ItineraryTabs.itinerarys = resp.data
        //                 })
        //                 .catch((err) => {
        //                     console.error(err);
        //                 });
        //         }
        //     })
        // })
    }
    else {
        // user has access token, user can open the page
        next(vm => {

            const headers = {
                "Content-Type": "application/json",
                Authorization: "Bearer " + access_token,
            };

            axios
                .get("http://127.0.0.1:8000/trip/itinerary/", {
                    headers,
                })
                .then((resp) => {
                    const ItineraryTabs = vm.$refs.ItineraryTabs;

                    ItineraryTabs.itinerarys = resp.data
                    ItineraryTabs.overlay = false;
                })
                .catch((err) => {
                    console.error(err);
                });
        })
    }


}

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            name: 'home',
            alias: ['/home', '/frontpage'],
            component: FrontPageRouter,
        },

        {
            path: '/schedule',
            name: 'schedule',
            component: ScheduleRouter,
            beforeEnter: (to, from, next) => {
                if (firstVisit && to.params.location === undefined) { // users do not provide any location on the first visit
                    next('/home')
                } else {
                    firstVisit = false;
                    next();
                }
            }
        },

        {
            path: '/itinerary',
            name: 'itinerary',
            component: ItineraryRouter,
            children: [
                {
                    path: ':id',
                    component: ItineraryTabItem,
                    props: true
                },
            ],
            // beforeEnter: (to, from, next) => {
            //     const access_token = Vue.cookie.get('access_token')

            //     if (access_token === null) {
            //         // user doesn't have access token, redirect to login
            //         next("/404")
            //     }
            //     else {
            //         // user has access token, user can open the page
            //         next()
            //     }
            // },
        },

        {
            path: '/404',
            alias: ['*'],
            name: 'pageNotFound',
            component: PageNotFoundRouter,
        },
    ]
})