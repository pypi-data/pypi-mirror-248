(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[327],{93808:function(t,e,r){"use strict";r.d(e,{Z:function(){return E}});var n=r(77837),u=r(26304),o=r(62243),i=r(29385),c=r(80022),s=r(13692),f=r(93189),a=r(15544),p=r(82394),l=r(38860),h=r.n(l),y=r(82684),v=r(56663),b=r.n(v),d=r(40761),O=r(34661),w=r(36105),Z=r(50178),g=r(69419),_=r(28598),P=["auth"];function j(t,e){var r=Object.keys(t);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(t);e&&(n=n.filter((function(e){return Object.getOwnPropertyDescriptor(t,e).enumerable}))),r.push.apply(r,n)}return r}function k(t){for(var e=1;e<arguments.length;e++){var r=null!=arguments[e]?arguments[e]:{};e%2?j(Object(r),!0).forEach((function(e){(0,p.Z)(t,e,r[e])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(r)):j(Object(r)).forEach((function(e){Object.defineProperty(t,e,Object.getOwnPropertyDescriptor(r,e))}))}return t}function m(t){var e=function(){if("undefined"===typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"===typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(t){return!1}}();return function(){var r,n=(0,a.Z)(t);if(e){var u=(0,a.Z)(this).constructor;r=Reflect.construct(n,arguments,u)}else r=n.apply(this,arguments);return(0,f.Z)(this,r)}}function E(t){return function(e){(0,s.Z)(f,e);var r=m(f);function f(){var t;(0,o.Z)(this,f);for(var e=arguments.length,n=new Array(e),u=0;u<e;u++)n[u]=arguments[u];return t=r.call.apply(r,[this].concat(n)),(0,p.Z)((0,c.Z)(t),"state",{auth:new d.Z(t.props.token)}),t}return(0,i.Z)(f,[{key:"componentDidMount",value:function(){this.setState({auth:new d.Z(this.props.token)})}},{key:"render",value:function(){var e=this.props,r=(e.auth,(0,u.Z)(e,P));return(0,_.jsx)(t,k({auth:this.state.auth},r))}}],[{key:"getInitialProps",value:function(){var e=(0,n.Z)(h().mark((function e(r){var n,u,o,i,c,s,f,a,p;return h().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(n=b()(r),u=(0,Z.ex)(r),o=u.id,i=n[O.Mv],c=n[w.qt],s=new d.Z(i),f=k(k({},r),{},{auth:s,currentGroupId:o,theme:c}),(0,Z.YB)(r)&&s.isExpired&&(console.log("OAuth token has expired."),a=k(k({},r.query),{},{redirect_url:r.asPath}),(0,g.nL)("/sign-in?".concat((0,g.uM)(a)),r.res)),!t.getInitialProps){e.next=12;break}return e.next=10,t.getInitialProps(f);case 10:return p=e.sent,e.abrupt("return",k(k({},p),{},{auth:s,currentGroupId:o,theme:c}));case 12:return e.abrupt("return",f);case 13:case"end":return e.stop()}}),e)})));return function(t){return e.apply(this,arguments)}}()}]),f}(y.Component)}},26450:function(t,e,r){"use strict";r.r(e);var n=r(77837),u=r(38860),o=r.n(u),i=r(82684),c=r(34376),s=r(93808);function f(t){var e=t.pipeline,r=(0,c.useRouter)();(0,i.useEffect)((function(){r.replace("/pipelines/[pipeline]/triggers","/pipelines/".concat(e.uuid,"/triggers"))}),[e])}f.getInitialProps=function(){var t=(0,n.Z)(o().mark((function t(e){var r;return o().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return r=e.query.pipeline,t.abrupt("return",{pipeline:{uuid:r}});case 2:case"end":return t.stop()}}),t)})));return function(e){return t.apply(this,arguments)}}(),e.default=(0,s.Z)(f)},67503:function(t,e,r){(window.__NEXT_P=window.__NEXT_P||[]).push(["/pipelines/[pipeline]",function(){return r(26450)}])},80022:function(t,e,r){"use strict";function n(t){if(void 0===t)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return t}r.d(e,{Z:function(){return n}})},15544:function(t,e,r){"use strict";function n(t){return n=Object.setPrototypeOf?Object.getPrototypeOf:function(t){return t.__proto__||Object.getPrototypeOf(t)},n(t)}r.d(e,{Z:function(){return n}})},13692:function(t,e,r){"use strict";r.d(e,{Z:function(){return u}});var n=r(61049);function u(t,e){if("function"!==typeof e&&null!==e)throw new TypeError("Super expression must either be null or a function");t.prototype=Object.create(e&&e.prototype,{constructor:{value:t,writable:!0,configurable:!0}}),e&&(0,n.Z)(t,e)}},93189:function(t,e,r){"use strict";r.d(e,{Z:function(){return o}});var n=r(12539),u=r(80022);function o(t,e){if(e&&("object"===n(e)||"function"===typeof e))return e;if(void 0!==e)throw new TypeError("Derived constructors may only return object or undefined");return(0,u.Z)(t)}},61049:function(t,e,r){"use strict";function n(t,e){return n=Object.setPrototypeOf||function(t,e){return t.__proto__=e,t},n(t,e)}r.d(e,{Z:function(){return n}})}},function(t){t.O(0,[9774,2888,179],(function(){return e=67503,t(t.s=e);var e}));var e=t.O();_N_E=e}]);