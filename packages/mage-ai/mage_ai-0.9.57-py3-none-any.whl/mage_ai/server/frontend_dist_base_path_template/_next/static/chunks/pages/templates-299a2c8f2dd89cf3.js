(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[5240],{60523:function(e,n,t){"use strict";var i=t(21831),r=t(82394),u=t(82684),o=t(38626),l=t(34376),d=t(54750),c=t(71180),s=t(90299),a=t(44898),f=t(55485),p=t(88328),h=t(38276),m=t(4190),v=t(48381),j=t(5755),b=t(30160),x=t(35686),g=t(72473),y=t(84649),Z=t(32929),w=t(15610),P=t(19183),O=t(28598);function C(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);n&&(i=i.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,i)}return t}function k(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?C(Object(t),!0).forEach((function(n){(0,r.Z)(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):C(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}n.Z=function(e){var n,t=e.contained,r=e.defaultLinkUUID,C=e.defaultTab,_=e.objectType,I=e.onClickCustomTemplate,T=e.pipelineUUID,A=e.showAddingNewTemplates,M=e.showBreadcrumbs,S=e.tabs,U=(0,l.useRouter)(),E=(0,u.useContext)(o.ThemeContext),N=(0,P.i)(),R=N.height,D=N.width,B=(0,u.useMemo)((function(){return S||Z.dP}),[S]),H=(0,u.useState)(A||!1),q=H[0],z=H[1],F=(0,u.useState)(r?Z.qy.find((function(e){return e.uuid===r})):Z.qy[0]),W=F[0],L=F[1],G=(0,u.useState)(C?B.find((function(e){return e.uuid===(null===C||void 0===C?void 0:C.uuid)})):B[0]),X=G[0],Y=G[1],V=(0,u.useState)(null),J=V[0],K=V[1],Q=x.ZP.custom_templates.list({object_type:a.Z},{},{pauseFetch:Z.n9.uuid!==(null===X||void 0===X?void 0:X.uuid)}),$=Q.data,ee=Q.mutate,ne=(0,u.useMemo)((function(){var e=(null===$||void 0===$?void 0:$.custom_templates)||[];return null!==W&&void 0!==W&&W.filterTemplates?null===W||void 0===W?void 0:W.filterTemplates(e):e}),[$,W]),te=x.ZP.custom_templates.list({object_type:a.R},{},{pauseFetch:Z.A2.uuid!==(null===X||void 0===X?void 0:X.uuid)}),ie=te.data,re=te.mutate,ue=(0,u.useMemo)((function(){var e=(null===ie||void 0===ie?void 0:ie.custom_templates)||[];return null!==W&&void 0!==W&&W.filterTemplates?null===W||void 0===W?void 0:W.filterTemplates(e):e}),[ie,W]),oe=(0,u.useMemo)((function(){return Z.qy.map((function(e){var n=e.Icon,t=e.label,i=e.selectedBackgroundColor,r=e.selectedIconProps,u=e.uuid,o=(null===W||void 0===W?void 0:W.uuid)===u,l=k({size:y.ZG},o&&r?r:{});return(0,O.jsx)(y.wj,{onClick:function(){return L(e)},selected:o,children:(0,O.jsxs)(f.ZP,{alignItems:"center",children:[(0,O.jsx)(y.ze,{backgroundColor:o&&i?i(E):null,children:n?(0,O.jsx)(n,k({},l)):(0,O.jsx)(g.pd,k({},l))}),(0,O.jsx)(b.ZP,{bold:!0,large:!0,children:t?t():u})]})},u)}))}),[W,E]),le=(0,u.useMemo)((function(){return Z.hS.map((function(e){var n=e.Icon,t=e.label,i=e.selectedBackgroundColor,r=e.selectedIconProps,u=e.uuid,o=(null===W||void 0===W?void 0:W.uuid)===u,l=k({size:y.ZG},o&&r?r:{});return(0,O.jsx)(y.wj,{onClick:function(){return L(e)},selected:o,children:(0,O.jsxs)(f.ZP,{alignItems:"center",children:[(0,O.jsx)(y.ze,{backgroundColor:o&&i?i(E):null,children:n?(0,O.jsx)(n,k({},l)):(0,O.jsx)(g.pd,k({},l))}),(0,O.jsx)(b.ZP,{bold:!0,large:!0,children:t?t():u})]})},u)}))}),[W,E]),de=(0,u.useMemo)((function(){return null===ne||void 0===ne?void 0:ne.map((function(e){var n=e.description,t=e.name,r=e.tags,u=e.template_uuid,o=e.user,l=[];return null!==r&&void 0!==r&&r.length?l.push.apply(l,(0,i.Z)(r)):null!==o&&void 0!==o&&o.username&&l.push(null===o||void 0===o?void 0:o.username),(0,O.jsxs)(y.UE,{onClick:function(){I?I(e):U.push("/templates/[...slug]","/templates/".concat(encodeURIComponent(u)))},children:[(0,O.jsx)(y.Tj,{children:(0,O.jsx)(b.ZP,{bold:!0,monospace:!0,textOverflow:!0,children:t||u})}),(0,O.jsx)(y.SL,{children:(0,O.jsx)(b.ZP,{default:!!n,italic:!n,muted:!n,textOverflowLines:2,children:n||"No description"})}),(0,O.jsx)(y.EN,{children:(null===l||void 0===l?void 0:l.length)>=1&&(0,O.jsx)(v.Z,{tags:null===l||void 0===l?void 0:l.map((function(e){return{uuid:e}}))})})]},u)}))}),[ne,I,U]),ce=(0,u.useMemo)((function(){return null===ue||void 0===ue?void 0:ue.map((function(e){var n=e.description,t=e.name,r=e.tags,u=e.template_uuid,o=e.user,l=[];return null!==r&&void 0!==r&&r.length?l.push.apply(l,(0,i.Z)(r)):null!==o&&void 0!==o&&o.username&&l.push(null===o||void 0===o?void 0:o.username),(0,O.jsxs)(y.UE,{onClick:function(){I?I(e):U.push("/templates/[...slug]","/templates/".concat(encodeURIComponent(u),"?object_type=").concat(a.R))},children:[(0,O.jsx)(y.Tj,{children:(0,O.jsx)(b.ZP,{bold:!0,monospace:!0,textOverflow:!0,children:t||u})}),(0,O.jsx)(y.SL,{children:(0,O.jsx)(b.ZP,{default:!!n,italic:!n,muted:!n,textOverflowLines:2,children:n||"No description"})}),(0,O.jsx)(y.EN,{children:(null===l||void 0===l?void 0:l.length)>=1&&(0,O.jsx)(v.Z,{tags:null===l||void 0===l?void 0:l.map((function(e){return{uuid:e}}))})})]},u)}))}),[ue,I,U]),se=(0,u.useMemo)((function(){if(!M)return null;var e=[];return q?e.push.apply(e,[{label:function(){return"Templates"},onClick:function(){z(!1)}},{bold:!0,label:function(){return"New custom template"}}]):e.push({label:function(){return"Templates"}}),(0,O.jsx)(y.FX,{children:(0,O.jsx)(d.Z,{breadcrumbs:e})})}),[q,M]),ae=(0,u.useMemo)((function(){return M?36:0}),[M]),fe=(0,u.useMemo)((function(){return R-ae}),[R,ae]);if(q)return n=a.R===_&&T?(0,O.jsx)(p.Z,{onMutateSuccess:re,pipelineUUID:T,templateAttributes:W&&(null===W||void 0===W?void 0:W.uuid)!==(null===Z.qy||void 0===Z.qy?void 0:Z.qy[0].uuid)?{pipeline_type:null===W||void 0===W?void 0:W.uuid}:null,templateUUID:null===J||void 0===J?void 0:J.template_uuid}):(0,O.jsx)(j.Z,{contained:t,heightOffset:ae,onCreateCustomTemplate:t?function(e){K(e)}:null,onMutateSuccess:ee,templateAttributes:W&&(null===W||void 0===W?void 0:W.uuid)!==(null===Z.qy||void 0===Z.qy?void 0:Z.qy[0].uuid)?{block_type:null===W||void 0===W?void 0:W.uuid}:null,templateUUID:null===J||void 0===J?void 0:J.template_uuid}),t?(0,O.jsxs)(O.Fragment,{children:[M&&se,(0,O.jsx)(y.Rd,{height:fe,width:D,children:n})]}):n;var pe=(0,O.jsxs)(y.Nk,{children:[(0,O.jsxs)(y.bC,{height:t?fe:null,children:[(0,O.jsx)(y.Yf,{children:(0,O.jsx)(s.Z,{noPadding:!0,onClickTab:function(e){t?Y(e):(0,w.u)({object_type:Z.A2.uuid===e.uuid?a.R:a.Z})},selectedTabUUID:null===X||void 0===X?void 0:X.uuid,tabs:B})}),(0,O.jsxs)(y.wl,{contained:t,heightOffset:ae,children:[Z.n9.uuid===(null===X||void 0===X?void 0:X.uuid)&&oe,Z.A2.uuid===(null===X||void 0===X?void 0:X.uuid)&&le]})]}),(0,O.jsxs)(y.w5,{children:[Z.n9.uuid===(null===X||void 0===X?void 0:X.uuid)&&(0,O.jsx)(y.HS,{children:(0,O.jsx)(c.ZP,{beforeIcon:(0,O.jsx)(g.mm,{size:y.ZG}),onClick:function(){z(!0)},primary:!0,children:"New block template"})}),Z.n9.uuid===(null===X||void 0===X?void 0:X.uuid)&&(0,O.jsxs)(O.Fragment,{children:[!$&&(0,O.jsx)(h.Z,{p:2,children:(0,O.jsx)(m.Z,{inverted:!0})}),$&&!(null!==de&&void 0!==de&&de.length)&&(0,O.jsxs)(h.Z,{p:2,children:[(0,O.jsx)(b.ZP,{children:"There are currently no templates matching your search."}),(0,O.jsx)("br",{}),(0,O.jsx)(b.ZP,{children:"Add a new template by clicking the button above."})]}),(null===de||void 0===de?void 0:de.length)>=1&&(0,O.jsx)(y.n8,{children:de})]}),Z.A2.uuid===(null===X||void 0===X?void 0:X.uuid)&&(0,O.jsxs)(O.Fragment,{children:[!ie&&(0,O.jsx)(h.Z,{p:2,children:(0,O.jsx)(m.Z,{inverted:!0})}),ie&&!(null!==ce&&void 0!==ce&&ce.length)&&(0,O.jsxs)(h.Z,{p:2,children:[(0,O.jsx)(b.ZP,{children:"There are currently no templates matching your search."}),(0,O.jsx)("br",{}),(0,O.jsx)(b.ZP,{children:'Add a new template by right-clicking a pipeline row from the Pipelines page and selecting "Create template".'})]}),(null===ce||void 0===ce?void 0:ce.length)>=1&&(0,O.jsx)(y.n8,{children:ce})]})]})]});return t?(0,O.jsxs)(O.Fragment,{children:[M&&se,(0,O.jsx)(y.Rd,{height:fe,width:D,children:pe})]}):pe}},94629:function(e,n,t){"use strict";t.d(n,{Z:function(){return C}});var i=t(82394),r=t(21831),u=t(82684),o=t(50724),l=t(82555),d=t(97618),c=t(70613),s=t(31557),a=t(68899),f=t(28598);function p(e,n){var t=e.children,i=e.noPadding;return(0,f.jsx)(a.HS,{noPadding:i,ref:n,children:t})}var h=u.forwardRef(p),m=t(62547),v=t(82571),j=t(98464),b=t(77417),x=t(46684),g=t(70515),y=t(53808),Z=t(19183);function w(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);n&&(i=i.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,i)}return t}function P(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?w(Object(t),!0).forEach((function(n){(0,i.Z)(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):w(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}function O(e,n){e.addProjectBreadcrumbToCustomBreadcrumbs;var t=e.after,i=e.afterHeader,p=e.afterHidden,w=e.afterWidth,O=e.afterWidthOverride,C=e.appendBreadcrumbs,k=e.before,_=e.beforeWidth,I=e.breadcrumbs,T=e.children,A=e.contained,M=e.errors,S=e.headerMenuItems,U=e.headerOffset,E=e.hideAfterCompletely,N=e.mainContainerHeader,R=e.navigationItems,D=e.setAfterHidden,B=e.setErrors,H=e.subheaderChildren,q=e.subheaderNoPadding,z=e.title,F=e.uuid,W=(0,Z.i)().width,L="dashboard_after_width_".concat(F),G="dashboard_before_width_".concat(F),X=(0,u.useRef)(null),Y=(0,u.useState)(O?w:(0,y.U2)(L,w)),V=Y[0],J=Y[1],K=(0,u.useState)(!1),Q=K[0],$=K[1],ee=(0,u.useState)(k?Math.max((0,y.U2)(G,_),13*g.iI):null),ne=ee[0],te=ee[1],ie=(0,u.useState)(!1),re=ie[0],ue=ie[1],oe=(0,u.useState)(null)[1],le=(0,b.Z)().project,de=[];I&&de.push.apply(de,(0,r.Z)(I)),null!==I&&void 0!==I&&I.length&&!C||!le||null!==I&&void 0!==I&&I.length||de.unshift({bold:!C,label:function(){return z}}),(0,u.useEffect)((function(){null===X||void 0===X||!X.current||Q||re||null===oe||void 0===oe||oe(X.current.getBoundingClientRect().width)}),[Q,V,re,ne,X,oe,W]),(0,u.useEffect)((function(){Q||(0,y.t8)(L,V)}),[p,Q,V,L]),(0,u.useEffect)((function(){re||(0,y.t8)(G,ne)}),[re,ne,G]);var ce=(0,j.Z)(w);return(0,u.useEffect)((function(){O&&ce!==w&&J(w)}),[O,w,ce]),(0,f.jsxs)(f.Fragment,{children:[(0,f.jsx)(c.Z,{title:z}),(0,f.jsx)(s.Z,{breadcrumbs:de,menuItems:S}),(0,f.jsxs)(a.Nk,{ref:n,children:[0!==(null===R||void 0===R?void 0:R.length)&&(0,f.jsx)(a.lm,{showMore:!0,children:(0,f.jsx)(v.Z,{navigationItems:R,showMore:!0})}),(0,f.jsx)(d.Z,{flex:1,flexDirection:"column",children:(0,f.jsxs)(m.Z,{after:t,afterHeader:i,afterHeightOffset:x.Mz,afterHidden:p,afterMousedownActive:Q,afterWidth:V,before:k,beforeHeightOffset:x.Mz,beforeMousedownActive:re,beforeWidth:a.k1+(k?ne:0),contained:A,headerOffset:U,hideAfterCompletely:!D||E,leftOffset:k?a.k1:null,mainContainerHeader:N,mainContainerRef:X,setAfterHidden:D,setAfterMousedownActive:$,setAfterWidth:J,setBeforeMousedownActive:ue,setBeforeWidth:te,children:[H&&(0,f.jsx)(h,{noPadding:q,children:H}),T]})})]}),M&&(0,f.jsx)(o.Z,{disableClickOutside:!0,isOpen:!0,onClickOutside:function(){return null===B||void 0===B?void 0:B(null)},children:(0,f.jsx)(l.Z,P(P({},M),{},{onClose:function(){return null===B||void 0===B?void 0:B(null)}}))})]})}var C=u.forwardRef(O)},48381:function(e,n,t){"use strict";var i=t(82684),r=t(31882),u=t(55485),o=t(30160),l=t(86735),d=t(28598);n.Z=function(e){var n=e.onClickTag,t=e.tags,c=void 0===t?[]:t,s=(0,i.useMemo)((function(){return(null===c||void 0===c?void 0:c.length)||0}),[c]),a=(0,i.useMemo)((function(){return(0,l.YC)(c||[],"uuid")}),[c]);return(0,d.jsx)(u.ZP,{alignItems:"center",flexWrap:"wrap",children:null===a||void 0===a?void 0:a.reduce((function(e,t){return e.push((0,d.jsx)("div",{style:{marginBottom:2,marginRight:s>=2?4:0,marginTop:2},children:(0,d.jsx)(r.Z,{onClick:n?function(){return n(t)}:null,small:!0,children:(0,d.jsx)(o.ZP,{children:t.uuid})})},"tag-".concat(t.uuid))),e}),[])})}},31882:function(e,n,t){"use strict";var i=t(38626),r=t(71180),u=t(55485),o=t(30160),l=t(44897),d=t(72473),c=t(70515),s=t(61896),a=t(28598),f=i.default.div.withConfig({displayName:"Chip__ChipStyle",componentId:"sc-1ok73g-0"})(["display:inline-block;"," "," "," "," "," ",""],(function(e){return!e.primary&&"\n    background-color: ".concat((e.theme.background||l.Z.background).tag,";\n  ")}),(function(e){return e.primary&&"\n    background-color: ".concat((e.theme.chart||l.Z.chart).primary,";\n  ")}),(function(e){return!e.small&&"\n    border-radius: ".concat((c.iI+s.Al)/2,"px;\n    height: ").concat(1.5*c.iI+s.Al,"px;\n    padding: ").concat(c.iI/1.5,"px ").concat(1.25*c.iI,"px;\n  ")}),(function(e){return e.small&&"\n    border-radius: ".concat((c.iI/2+s.Al)/2,"px;\n    height: ").concat(s.Al+c.iI/2+2,"px;\n    padding: ").concat(c.iI/4,"px ").concat(c.iI,"px;\n  ")}),(function(e){return e.xsmall&&"\n    border-radius: ".concat((c.iI/1+s.Al)/1,"px;\n    height: ").concat(20,"px;\n    padding: 4px 6px;\n  ")}),(function(e){return e.border&&"\n    border: 1px solid ".concat((e.theme.content||l.Z.content).muted,";\n  ")}));n.Z=function(e){var n=e.border,t=e.children,i=e.disabled,l=e.label,s=e.monospace,p=e.onClick,h=e.primary,m=e.small,v=e.xsmall;return(0,a.jsx)(f,{border:n,primary:h,small:m,xsmall:v,children:(0,a.jsx)(r.ZP,{basic:!0,disabled:i,noBackground:!0,noPadding:!0,onClick:p,transparent:!0,children:(0,a.jsxs)(u.ZP,{alignItems:"center",children:[t,l&&(0,a.jsx)(o.ZP,{monospace:s,small:m,xsmall:v,children:l}),!i&&p&&(0,a.jsx)("div",{style:{marginLeft:2}}),!i&&p&&(0,a.jsx)(d.x8,{default:h,muted:!h,size:m?c.iI:1.25*c.iI})]})})})}},60820:function(e,n,t){"use strict";t.r(n);var i=t(77837),r=t(38860),u=t.n(r),o=t(82684),l=t(60523),d=t(94629),c=t(93808),s=t(32929),a=t(44898),f=t(69419),p=t(28598);function h(){var e=(0,o.useState)(!1),n=e[0],t=e[1],i=(0,o.useState)(null),r=i[0],u=i[1],c=(0,o.useState)(null),h=c[0],m=c[1],v=(0,f.iV)();(0,o.useEffect)((function(){var e=v.new,n=v.object_type,i=v.pipeline_uuid;n&&u(n),i&&m(i),t(!!e)}),[v]);var j=(0,o.useMemo)((function(){var e=[n?"New":"Browse"];return r&&e.push(r),h&&e.push(h),e}),[n,r,h]),b=(0,o.useMemo)((function(){return a.R===r}),[r]);return(0,p.jsx)(d.Z,{addProjectBreadcrumbToCustomBreadcrumbs:n,breadcrumbs:n?[{label:function(){return"Templates"},linkProps:{href:b?"/templates?object_type=".concat(a.R):"/templates"}},{bold:!0,label:function(){return"New"}}]:null,title:"Templates",uuid:"Templates/index",children:(0,p.jsx)(l.Z,{defaultTab:b?s.A2:null,objectType:r,pipelineUUID:h,showAddingNewTemplates:n},j.join("_"))})}h.getInitialProps=(0,i.Z)(u().mark((function e(){return u().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.abrupt("return",{});case 1:case"end":return e.stop()}}),e)}))),n.default=(0,c.Z)(h)},87710:function(e,n,t){(window.__NEXT_P=window.__NEXT_P||[]).push(["/templates",function(){return t(60820)}])}},function(e){e.O(0,[2678,1154,844,5820,6639,1124,1751,341,1821,874,1557,8264,7858,5499,5283,3745,5810,3859,2646,8998,3004,9264,9774,2888,179],(function(){return n=87710,e(e.s=n);var n}));var n=e.O();_N_E=n}]);