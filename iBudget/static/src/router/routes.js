import {Home, Funds, Groups, Spendings, Incomes} from 'src/tabs';
import {Login, Spending_registration, Spend, Limit, Icon_getter, Spending_add, Financial_goal,
        Funds_registration, Spending_history, PasswordRecovery, Income_registration,  Income_tracker,
        Groups_registration, Goal, Income_add} from "src/components";


export default [
    //login
    {
        path: '/password_recovery', component: PasswordRecovery
    },
    {
        path: '/password_recovery/:token', component: PasswordRecovery
    },
    {
        path: '/', redirect: '/login'
    },
    //tabs
    {
        path: '/incomes', component: Incomes,
        children:[
         {
        path: 'tracking', component: Income_tracker
    },

    {
        path: 'add', component: Income_registration
    },

    {
        path: 'new', component: Income_add
    }
        ]
    },
    {
        path: '/home', component: Home
    },
    {
        path: '/funds', component: Funds,
        children:[
        {
        path: 'new', component: Funds_registration
    },
    {
        path: 'new_goal', component:Financial_goal
    },
      {
        path: 'tracking_goal', component: Goal
    },

        ]
    },
    {
        path: '/groups', component: Groups
    },
    {
        path: '/spendings', component: Spendings,
        children: [
            {
                path: 'add', component: Spending_registration
            },
            {
                path: 'limit_ind', component: Spend
            },
            {
                path: 'limit_group', component: Limit
            },
            {
                path: 'new', component: Spending_add
            },
            {
                 path: 'history', component: Spending_history
            },
        ]
    },
    {
        path: '/login', component: Login
    },

    //Group
    {
        path: '/groups/add', component: Groups_registration
    },



];
