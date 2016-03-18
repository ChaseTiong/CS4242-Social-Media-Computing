var app = angular.module('cs4242', ['ngRoute','ngResource']);

// app.config(['$routeProvider',
//   function($routeProvider) {
//     $routeProvider.
//       when('/', {
//         templateUrl: 'partials/home.html',
//         controller: 'HomeCtrl',
//         activeTab: 'home'
//       }).
//       when('/schema',{
//         templateUrl: 'partials/schedule.html',
//         controller: 'ScheduleCtrl',
//         activeTab: 'schedule'
//       }). 
//       when('/prislista', {
//         templateUrl: 'partials/prices.html',
//         controller: 'PricesCtrl',
//         activeTab: 'prices'
//       }).
//       when('/kontakt',{
//         templateUrl: 'partials/contact.html',
//         controller: 'ContactCtrl',
//         activeTab: 'contact'
//       }).
//       when('/intervjuer',{
//         templateUrl: 'partials/jobs.html',
//         controller: 'JobsCtrl',
//         activeTab: 'interviews'
//       }).
//       when('/intervjuer/:jobID',{
//         templateUrl: 'partials/job.html',
//         controller: 'SingleJobCtrl',
//         activeTab: 'interviews'
//       }).
//       when('/foretag/:companyName',{
//         templateUrl: 'partials/company.html',
//         controller: 'CompanyCtrl'
//       }).
//       when('/monterplatser', {
//         templateUrl: 'partials/map.html',
//         controller: 'MapCtrl',
//         activeTab: 'map'
//       }).
//       when('/prislista/:packageType', {
//         templateUrl: 'partials/package.html',
//         controller: 'PackageCtrl',
//         activeTab: 'prices'
//       }).
//       otherwise({
//         redirectTo: '/'
//       });
//   }])