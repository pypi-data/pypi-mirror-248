"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[8998],{27277:function(e,n,t){var r=t(82394),i=t(21831),o=t(82684),l=t(39643),c=t(44688),u=t(28598);function a(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function d(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?a(Object(t),!0).forEach((function(n){(0,r.Z)(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):a(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}n.Z=function(e){var n=e.highlightedItemIndexInitial,t=void 0===n?null:n,r=e.itemGroups,a=e.noResultGroups,s=e.onHighlightItemIndexChange,f=e.onMouseEnterItem,v=e.onMouseLeaveItem,p=e.onSelectItem,h=e.renderEmptyState,j=e.searchQuery,m=e.selectedItem,x=e.setItemRefs,b=e.uuid,g=(0,o.useState)(!0),Z=g[0],y=g[1],O=(0,o.useMemo)((function(){var e=[],n=r.reduce((function(n,t){var r=t.items.filter((function(e){return!j||function(e,n){return e.searchQueries.filter((function(e){return String(e).toLowerCase().includes(n.toLowerCase())})).length>=1}(e,j)}));return 0===r.length?n:(e.push.apply(e,(0,i.Z)(r)),n.concat(d(d({},t),{},{items:r})))}),[]);return{itemGroups:n,itemsFlattened:e}}),[r,j]),I=O.itemGroups,P=O.itemsFlattened;a&&0===P.length&&(I.push.apply(I,(0,i.Z)(a)),P.push.apply(P,(0,i.Z)(a.reduce((function(e,n){var t=n.items;return e.concat(t)}),[]))));var E=(0,o.useRef)(null);E.current=P.map((function(){return(0,o.createRef)()}));var w=(0,o.useState)(t),D=w[0],C=w[1],S=(0,o.useCallback)((function(e){null===s||void 0===s||s(e),C(e)}),[s,C]),k=P[D],L=(0,c.y)(),R=L.registerOnKeyDown,T=L.unregisterOnKeyDown;(0,o.useEffect)((function(){return function(){return T(b)}}),[T,b]),null===R||void 0===R||R(b,(function(e,n,t){var r,i=!0,o=P.length,c=P.findIndex((function(e,r){var i=e.keyboardShortcutValidation;return null===i||void 0===i?void 0:i({keyHistory:t,keyMapping:n},r)})),u=n[l.Gs]&&!n[l.XR]&&!m;return-1!==c?(e.preventDefault(),p(P[c]),y(i),S(c)):(n[l.Uq]||u)&&P[D]?(u&&e.preventDefault(),p(P[D]),y(i),S(D)):(n[l.Bu]?(i=!1,r=null===D?o-1:D-1):n[l.kD]?(i=!1,r=null===D?0:D+1):n[l.vP]&&S(null),"undefined"!==typeof r&&(r>=o?r=0:r<=-1&&(r=o-1),r>=0&&r<=o-1?(S(r),e.preventDefault()):S(null)),void y(i))}),[D,P,m,S,y]),(0,o.useEffect)((function(){null===x||void 0===x||x(E)}),[E,P,x]),(0,o.useEffect)((function(){var e=null===D||"undefined"===typeof D||D>=P.length;(null===j||void 0===j?void 0:j.length)>=1&&e&&S(0)}),[D,P,j,S]);var M=(0,o.useCallback)((function(){return y(!0)}),[y]);return(0,o.useEffect)((function(){return window.addEventListener("mousemove",M),function(){window.removeEventListener("mousemove",M)}}),[M]),0===I.length&&h?h():(0,u.jsx)(u.Fragment,{children:I.map((function(e,n){var t=e.items,r=e.renderItem,i=e.renderGroupHeader,o=e.uuid,l=n>=1?I.slice(0,n).reduce((function(e,n){return e+n.items.length}),0):0,c=t.map((function(e,n){var t=e.itemObject,i=e.value,o=i===(null===k||void 0===k?void 0:k.value),c=n+l,a=(null===t||void 0===t?void 0:t.id)||(null===t||void 0===t?void 0:t.uuid);return(0,u.jsx)("div",{id:"item-".concat(i,"-").concat(a),onMouseMove:function(){return Z&&S(c)},ref:E.current[c],children:r(e,{highlighted:o,onClick:function(){return p(e)},onMouseEnter:function(){return null===f||void 0===f?void 0:f(e)},onMouseLeave:function(){return null===v||void 0===v?void 0:v(e)}},n,c)},"item-".concat(i,"-").concat(a))}));return c.length>=1&&(0,u.jsxs)("div",{children:[null===i||void 0===i?void 0:i(),c]},o||"group-uuid-".concat(n))}))})}},81769:function(e,n,t){t.d(n,{Z:function(){return re}});var r=t(82394),i=t(82684),o=t(85854),l=t(21831),c=t(65701),u=t(1254),a=t(97618),d=t(55485),s=t(70652),f=t(54193),v=t(44085),p=t(38276),h=t(30160),j=t(35576),m=t(17488),x=t(69650),b=t(70515),g=t(28598);function Z(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function y(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?Z(Object(t),!0).forEach((function(n){(0,r.Z)(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):Z(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}var O=function(e){var n=e.interaction,t=e.setVariables,o=e.showVariableUUID,l=e.variables,c=n||{inputs:{},layout:[],variables:{}},u=c.inputs,Z=c.layout,O=c.variables,I=(0,i.useMemo)((function(){var e=[];return null===Z||void 0===Z||Z.forEach((function(n,c){var Z=[];null===n||void 0===n||n.forEach((function(e,n){var c,I=e.variable,P=(e.width,(null===O||void 0===O?void 0:O[I])||{uuid:I}),E=P.description,w=P.input,D=P.name,C=P.required,S=(null===u||void 0===u?void 0:u[w])||{options:[],style:null,type:null},k=S.options,L=S.style,R=S.type,T="".concat(I,"-").concat(R),M={required:C},A=[],_="undefined"!==typeof l?null===l||void 0===l?void 0:l[I]:void 0;if(f.bB.CHECKBOX===R)A.push((0,g.jsx)(d.ZP,{alignItems:"center",children:null===k||void 0===k?void 0:k.map((function(e){var n=e.label,i=e.value,o=(null===l||void 0===l?void 0:l[I])||{};console.log(i,o);var c=(null===o||void 0===o?void 0:o[i])||(null===o||void 0===o?void 0:o[String(i)]);return(0,g.jsx)(p.Z,{mr:b.cd,children:(0,g.jsx)(s.Z,y(y({},M),{},{label:n,checked:!!c,onClick:function(){return null===t||void 0===t?void 0:t((function(e){return y(y({},e),{},(0,r.Z)({},I,y(y({},o),{},(0,r.Z)({},i,!c))))}))}}))},String(i||n))}))},"".concat(T,"-").concat(R)));else if(f.bB.TEXT_FIELD===R)A.push((0,g.jsx)(d.ZP,{flexDirection:"column",children:null!==L&&void 0!==L&&L.multiline?(0,i.createElement)(j.Z,y(y({},M),{},{key:"".concat(T,"-").concat(R),onChange:function(e){return null===t||void 0===t?void 0:t((function(n){return y(y({},n),{},(0,r.Z)({},I,e.target.value))}))},value:_})):(0,i.createElement)(m.Z,y(y({},M),{},{key:"".concat(T,"-").concat(R),onChange:function(e){return null===t||void 0===t?void 0:t((function(n){return y(y({},n),{},(0,r.Z)({},I,e.target.value))}))},type:(null===L||void 0===L?void 0:L.input_type)||null,value:_}))},"".concat(T,"-").concat(R)));else if(f.bB.DROPDOWN_MENU===R)A.push((0,i.createElement)(v.Z,y(y({},M),{},{key:"".concat(T,"-").concat(R),onChange:function(e){return null===t||void 0===t?void 0:t((function(n){return y(y({},n),{},(0,r.Z)({},I,e.target.value))}))},value:_}),(0,g.jsx)("option",{value:""}),null===k||void 0===k?void 0:k.map((function(e){var n=e.label,t=e.value;return(0,g.jsx)("option",{value:String(t||n),children:String(n||t)},String(t||n))}))));else if(f.bB.SWITCH===R){var N;Z.push((0,g.jsx)(p.Z,{mt:n>=1?b.cd:0,children:(0,g.jsxs)(d.ZP,{alignItems:"center",fullWidth:!0,children:[(0,i.createElement)(x.Z,y(y({},M),{},{checked:_,compact:!0,key:"".concat(T,"-").concat(R),onCheck:function(e){return null===t||void 0===t?void 0:t((function(n){return y(y({},n),{},(0,r.Z)({},I,e(_)))}))}})),(D||E)&&(0,g.jsx)(p.Z,{ml:b.cd}),(D||E||o)&&(0,g.jsxs)(d.ZP,{alignItems:"flex-start",flexDirection:"row",fullWidth:!0,justifyContent:"space-between",children:[(D||E)&&(0,g.jsxs)(a.Z,{flex:1,flexDirection:"column",children:[D&&(0,g.jsx)(h.ZP,{bold:!0,large:!0,success:!0,children:D}),E&&(null===E||void 0===E||null===(N=E.split("\n"))||void 0===N?void 0:N.map((function(e){return(0,g.jsx)(h.ZP,{default:!0,children:e},e)})))]}),o&&(0,g.jsxs)(g.Fragment,{children:[(0,g.jsx)(p.Z,{mr:b.cd}),(0,g.jsx)(h.ZP,{monospace:!0,muted:!0,small:!0,children:I})]})]})]})},T))}(null===A||void 0===A?void 0:A.length)>=1&&Z.push((0,g.jsxs)(p.Z,{mt:n>=1?b.cd:0,children:[(D||E||o)&&(0,g.jsxs)(d.ZP,{alignItems:"flex-start",justifyContent:"space-between",children:[(0,g.jsx)(a.Z,{flex:1,flexDirection:"column",children:(0,g.jsxs)(p.Z,{mb:1,children:[D&&(0,g.jsx)(h.ZP,{bold:!0,large:!0,success:!0,children:D}),E&&(null===E||void 0===E||null===(c=E.split("\n"))||void 0===c?void 0:c.map((function(e){return(0,g.jsx)(h.ZP,{default:!0,children:e},e)})))]})}),(0,g.jsx)(p.Z,{mr:b.cd}),o&&(0,g.jsx)(h.ZP,{monospace:!0,muted:!0,small:!0,children:I})]}),A]},T))})),e.push((0,g.jsx)(p.Z,{mt:c>=1?b.Mq:0,children:Z},"row-".concat(c)))})),e}),[u,Z,t,o,O,l]);return(0,g.jsx)(g.Fragment,{children:I})},I=t(72473),P=t(38626),E=t(44897),w=t(42631),D=t(55283),C=(b.iI,P.default.div.withConfig({displayName:"indexstyle__ContainerStyle",componentId:"sc-1ry80xj-0"})([""," border-radius:","px;position:relative;border-style:solid;border-width:1px;overflow:hidden;",""],D.Kf,w.n_,(function(e){return"\n    background-color: ".concat((e.theme.background||E.Z.background).panel,";\n  ")}))),S=P.default.div.withConfig({displayName:"indexstyle__HeadlineStyle",componentId:"sc-1ry80xj-1"})(["",""],(function(e){return"\n    background-color: ".concat((e.theme.background||E.Z.background).chartBlock,";\n  ")})),k=P.default.div.withConfig({displayName:"indexstyle__DottedLineStyle",componentId:"sc-1ry80xj-2"})(["",""],(function(e){return"\n    border: 1px dashed ".concat((e.theme.borders||E.Z.borders).light,";\n  ")})),L=P.default.div.withConfig({displayName:"indexstyle__LayoutItemStyle",componentId:"sc-1ry80xj-3"})(["",""],(function(e){return!e.disableDrag&&"\n    &:hover {\n      cursor: move;\n    }\n  "}));var R=function(e){var n=e.columnLayoutSettings,t=e.drag,i=e.drop,o=e.input,l=e.setVariables,c=e.showVariableUUID,u=e.variable,a=e.variables,d=e.width,s=null===u||void 0===u?void 0:u.input,f=null===n||void 0===n?void 0:n.variable;return(0,g.jsx)(L,{disableDrag:!t,ref:i,style:{width:d},children:(0,g.jsx)(C,{ref:t,style:{marginLeft:b.iI,marginRight:b.iI},children:(0,g.jsxs)(p.Z,{p:b.cd,children:[!!t&&(0,g.jsx)(p.Z,{mb:1,children:(0,g.jsx)(I.o0,{default:!0,size:2*b.iI})}),(0,g.jsx)(O,{interaction:{inputs:(0,r.Z)({},s,o),layout:[[{variable:f,width:1}]],variables:(0,r.Z)({},f,u)},setVariables:l,showVariableUUID:c,variables:a})]})})})},T=t(75582),M=t(26304),A=t(10975),_=t(14567),N=["columnIndex","columnsInRow","onDrop","rowIndex"];function B(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function U(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?B(Object(t),!0).forEach((function(n){(0,r.Z)(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):B(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}var G=function(e){var n=e.columnIndex,t=(e.columnsInRow,e.onDrop),r=e.rowIndex,i=(0,M.Z)(e,N),o=(0,A.c)((function(){return{collect:function(e){return{isDragging:!!e.isDragging()}},item:{columnIndex:n,rowIndex:r},type:"InteractionLayoutItem"}}),[n,r]),l=(0,T.Z)(o,2),c=(l[0],l[1]),u=(0,_.L)((function(){return{accept:"InteractionLayoutItem",drop:function(e){return null===t||void 0===t?void 0:t(e)}}}),[t]),a=(0,T.Z)(u,2)[1];return(0,g.jsx)(R,U(U({},i),{},{drag:c,drop:a}))};var F=function(e){var n=e.children,t=e.onDrop,r=e.width,i=(0,_.L)((function(){return{accept:"InteractionLayoutItem",drop:function(e){return null===t||void 0===t?void 0:t(e)}}}),[t]),o=(0,T.Z)(i,2)[1];return(0,g.jsx)("div",{ref:o,style:{width:r},children:(0,g.jsxs)(p.Z,{p:b.cd,children:[n,(0,g.jsx)(k,{})]})})},V=t(86735),W=t(19183);var q=function(e){var n=e.containerRef,t=e.containerWidth,r=e.interaction,o=e.setVariables,s=e.showVariableUUID,f=e.updateLayout,v=e.variables,h=e.widthOffset,j=(0,W.i)(),m=(0,i.useState)(null),x=m[0],b=m[1];(0,i.useEffect)((function(){var e;null!==n&&void 0!==n&&n.current?b(null===n||void 0===n||null===(e=n.current)||void 0===e?void 0:e.getBoundingClientRect()):t&&b({width:t})}),[t,n,j]);var Z=(0,i.useMemo)((function(){return{inputs:null===r||void 0===r?void 0:r.inputs,layout:null===r||void 0===r?void 0:r.layout,variables:null===r||void 0===r?void 0:r.variables}}),[r]),y=Z.inputs,O=Z.layout,I=Z.variables,P=(0,i.useCallback)((function(e,n,t,r,i){var o=(0,l.Z)(O||[]),c=o[e]||[],u=c[n];if(null!==i&&void 0!==i&&i.newRow){var a,d=(0,V.oM)(c,n);return o[e]=d,-1===t?o.unshift([u]):t>=(null===(a=o)||void 0===a?void 0:a.length)?o.push([u]):o=(0,V.VS)([u],t,o),0===(null===d||void 0===d?void 0:d.length)&&(o=(0,V.oM)(o,t<e?e+1:e)),void(null===f||void 0===f||f(o))}if(e===t&&n!==r){var s=(0,V.oM)(c,n);o[e]=(0,V.Hk)(u,r>n?r:r-1,s)}else{var v=(0,V.oM)(c,n);o[e]=v;var p=(0,V.Hk)(u,r,o[t]);o[t]=p,0===(null===v||void 0===v?void 0:v.length)&&(o=(0,V.oM)(o,e))}e===t&&n===r||null===f||void 0===f||f(o)}),[O,f]),E=(0,i.useMemo)((function(){return(null===O||void 0===O?void 0:O.length)||0}),[O]),w=(0,i.useMemo)((function(){var e=[];return null===O||void 0===O||O.forEach((function(n,t){var r=(null===n||void 0===n?void 0:n.length)||0,i=[],l=(0,V.Sm)(null===n||void 0===n?void 0:n.map((function(e){return e.width||0}))),c=(null===n||void 0===n?void 0:n.length)||0,u=null===x||void 0===x?void 0:x.width;null===n||void 0===n||n.forEach((function(e,n){var d=e||{variable:null,width:0},p=d.variable,j=d.max_width_percentage,m=d.width,x=null===I||void 0===I?void 0:I[p],b=null===y||void 0===y?void 0:y[null===x||void 0===x?void 0:x.input],Z="undefined"!==typeof j&&null!==j?j>=0?j/100:j:null,O=m/l,E=Z&&O>Z?Z:O,w=f?G:R,D=Math.floor(E*u)-("undefined"===typeof h||null===h?f?Math.round(24/r):Math.round(50/r):Math.round(h/r));i.push((0,g.jsx)(a.Z,{flexBasis:"".concat(Math.floor(100*E),"%"),children:(0,g.jsx)(w,{columnIndex:n,columnLayoutSettings:e,columnsInRow:c,disableDrag:!!f,first:0===n,input:b,onDrop:function(e){var r=e.columnIndex,i=e.rowIndex;P(i,r,t,n)},rowIndex:t,setVariables:o,showVariableUUID:s,variable:x,variables:v,width:D})},"row-".concat(t,"-column-").concat(n,"-").concat(p)))})),0===t&&f&&e.push((0,g.jsx)(F,{onDrop:function(e){var n=e.columnIndex,r=e.rowIndex;P(r,n,t-1,0,{newRow:!0})}},"layout-divider-".concat(t,"-top"))),e.push((0,g.jsx)(d.ZP,{children:i},"row-".concat(t))),f?e.push((0,g.jsx)(F,{onDrop:function(e){var n=e.columnIndex,r=e.rowIndex;P(r,n,t+1,0,{newRow:!0})}},"layout-divider-".concat(t,"-bottom"))):t<E-1&&e.push((0,g.jsx)(p.Z,{py:2},"layout-divider-".concat(t,"-bottom")))})),e}),[x,y,O,P,E,o,s,f,I,v,h]);return f?(0,g.jsx)(c.W,{backend:u.PD,children:w}):(0,g.jsx)(g.Fragment,{children:w})},H=t(32013),K=t(98777),Y=t(71180),X=t(15338),z=t(81728),Q=t(95924);function J(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function $(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?J(Object(t),!0).forEach((function(n){(0,r.Z)(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):J(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}var ee=function(e){var n,t,c,u,Z=e.children,y=e.containerWidth,P=e.interaction,E=e.removeBlockInteraction,w=e.updateInteraction,D=(0,i.useRef)(null),k=(0,i.useRef)(null),L=(0,i.useRef)(null),R=(0,i.useRef)(null),M=(0,i.useRef)(null),A=(0,i.useState)(!1),_=A[0],N=A[1],B=(0,i.useState)(!1),U=B[0],G=B[1],F=(0,i.useState)(null),W=F[0],J=F[1],ee=(0,i.useState)(null),ne=ee[0],te=ee[1],re=(0,i.useState)(null),ie=re[0],oe=re[1],le=(0,i.useState)(null),ce=le[0],ue=le[1],ae=(0,i.useState)(null),de=ae[0],se=ae[1],fe=(0,i.useState)({}),ve=fe[0],pe=fe[1],he=P||{layout:null,variables:null,uuid:null},je=he.inputs,me=he.layout,xe=he.uuid,be=he.variables,ge=(0,i.useCallback)((function(e){return w($($({},P),e))}),[P,w]),Ze=(0,i.useCallback)((function(e,n){var t=$({},be),r=$({},je);return!n?(delete r[e],Object.entries(t||{}).forEach((function(n){var r=(0,T.Z)(n,2),i=r[0],o=r[1];e===(null===o||void 0===o?void 0:o.input)&&(t[i]=$($({},o),{},{input:null}))}))):r[e]=$($({},null===r||void 0===r?void 0:r[e]),n),ge({inputs:r})}),[je,ge,be]),ye=(0,i.useCallback)((function(e,n){var t=[],r=$({},be),i=!n;return i?delete r[e]:r[e]=$($({},null===r||void 0===r?void 0:r[e]),n),null===me||void 0===me||me.forEach((function(n){var r=[];null===n||void 0===n||n.forEach((function(n){i&&e===(null===n||void 0===n?void 0:n.variable)||r.push(n)})),(null===r||void 0===r?void 0:r.length)>=1&&t.push(r)})),ge({layout:t,variables:r})}),[me,ge,be]),Oe=(0,i.useMemo)((function(){return Object.entries(je||{}).map((function(e,n){var t=(0,T.Z)(e,2),r=t[0],i=t[1]||{options:[],style:null,type:null},o=i.options,l=i.style,c=i.type;return(0,g.jsx)(p.Z,{mt:n>=1?b.cd:0,children:(0,g.jsxs)(C,{ref:W===r?k:null,children:[(0,g.jsx)(S,{children:(0,g.jsx)(p.Z,{p:b.cd,children:(0,g.jsxs)(d.ZP,{alignItems:"center",justifyContent:"space-between",children:[(0,g.jsx)(h.ZP,{large:!0,monospace:!0,children:r}),(0,g.jsx)(p.Z,{mr:b.cd}),(0,g.jsx)(Y.ZP,{iconOnly:!0,noBackground:!0,noBorder:!0,noPadding:!0,onClick:function(){return Ze(r,null)},children:(0,g.jsx)(I.x8,{default:!0})})]})})}),(0,g.jsx)(X.Z,{muted:!0}),(0,g.jsx)(p.Z,{p:b.cd,children:(0,g.jsxs)(d.ZP,{fullWidth:!0,children:[(0,g.jsxs)(a.Z,{flex:1,flexDirection:"column",children:[(0,g.jsx)(p.Z,{mb:1,children:(0,g.jsx)(h.ZP,{bold:!0,default:!0,children:"Type"})}),(0,g.jsx)(v.Z,{onChange:function(e){return Ze(r,{type:e.target.value})},placeholder:"Choose a type of input",value:c,children:f.qS.map((function(e){return(0,g.jsx)("option",{value:e,children:(0,z.vg)(e)},e)}))})]}),(0,g.jsx)(p.Z,{mr:b.Mq}),(0,g.jsxs)(a.Z,{flex:1,flexDirection:"column",children:[f.bB.TEXT_FIELD===c&&(0,g.jsxs)(g.Fragment,{children:[(0,g.jsxs)(p.Z,{mb:b.cd,children:[(0,g.jsx)(p.Z,{mb:1,children:(0,g.jsxs)(h.ZP,{bold:!0,default:!0,children:["Style ",(0,z.J3)(c)]})}),(0,g.jsx)(s.Z,{checked:null===l||void 0===l?void 0:l.multiline,label:"Allow writing multiple lines",onClick:function(){return Ze(r,{style:$($({},l),{},{multiline:!(null!==l&&void 0!==l&&l.multiline)})})}})]}),(0,g.jsxs)("div",{children:[(0,g.jsxs)(p.Z,{mb:1,children:[(0,g.jsx)(h.ZP,{bold:!0,default:!0,children:"Text field type"}),(null===l||void 0===l?void 0:l.multiline)&&(0,g.jsx)(h.ZP,{muted:!0,small:!0,children:"Not available for multiline text field."})]}),(0,g.jsx)(s.Z,{checked:f.al.NUMBER===(null===l||void 0===l?void 0:l.input_type),disabled:!(null===l||void 0===l||!l.multiline),label:"Numbers only",onClick:function(){return Ze(r,{style:$($({},l),{},{input_type:f.al.NUMBER===(null===l||void 0===l?void 0:l.input_type)?null:f.al.NUMBER})})}})]})]}),[f.bB.CHECKBOX,f.bB.DROPDOWN_MENU].includes(c)&&(0,g.jsxs)(g.Fragment,{children:[(0,g.jsx)(p.Z,{mb:1,children:(0,g.jsxs)(h.ZP,{bold:!0,default:!0,children:["Options for ",(0,z.J3)(c)]})}),null===o||void 0===o?void 0:o.map((function(e,n){var t=e.label,i=e.value;return(0,g.jsx)(p.Z,{mt:n>=1?1:0,children:(0,g.jsxs)(d.ZP,{alignItems:"center",flexDirection:"row",children:[(0,g.jsx)(Y.ZP,{iconOnly:!0,noBackground:!0,noBorder:!0,onClick:function(){return Ze(r,{options:(0,V.oM)(o,n)})},children:(0,g.jsx)(I.x8,{})}),(0,g.jsx)(p.Z,{mr:b.cd}),(0,g.jsx)(h.ZP,{default:!0,children:"Label"}),(0,g.jsx)(p.Z,{mr:1}),(0,g.jsx)(m.Z,{compact:!0,onChange:function(e){var t;return Ze(r,{options:null===(t=o||[])||void 0===t?void 0:t.map((function(t,r){return n===r?$($({},t),{},{label:e.target.value}):t}))})},value:t||""}),(0,g.jsx)(p.Z,{mr:b.cd}),(0,g.jsx)(h.ZP,{default:!0,children:"Value"}),(0,g.jsx)(p.Z,{mr:1}),(0,g.jsx)(m.Z,{compact:!0,onChange:function(e){var t;return Ze(r,{options:null===(t=o||[])||void 0===t?void 0:t.map((function(t,r){return n===r?$($({},t),{},{value:e.target.value}):t}))})},value:i||""})]})},"".concat(r,"-option-").concat(n))})),(0,g.jsx)(p.Z,{mt:1,children:(0,g.jsx)(Y.ZP,{beforeIcon:(0,g.jsx)(I.mm,{}),compact:!0,onClick:function(){return Ze(r,{options:(o||[]).concat({label:"",value:""})})},secondary:!0,children:"Add option"})})]})]})]})})]})},"".concat(r,"-").concat(n))}))}),[je,W,k,Ze]),Ie=(0,i.useMemo)((function(){return Object.entries(be||{}).map((function(e,n){var t,i=(0,T.Z)(e,2),o=i[0],l=i[1],c=l||{description:"",name:"",required:!1,types:[]},u=c.description,Z=c.input,y=c.name,P=c.required,E=c.types,w=null===je||void 0===je?void 0:je[Z];return(0,g.jsx)(p.Z,{mt:n>=1?b.cd:0,children:(0,g.jsxs)(C,{ref:ne===o?L:null,children:[(0,g.jsx)(S,{children:(0,g.jsx)(p.Z,{p:b.cd,children:(0,g.jsxs)(d.ZP,{alignItems:"center",justifyContent:"space-between",children:[(0,g.jsxs)(d.ZP,{alignItems:"center",flexDirection:"row",children:[(0,g.jsx)(h.ZP,{large:!0,monospace:!0,children:o}),(0,g.jsx)(p.Z,{mr:b.cd}),(0,g.jsxs)(d.ZP,{alignItems:"center",children:[(0,g.jsx)(x.Z,{checked:P,compact:!0,onCheck:function(e){return ye(o,{required:e(P)})}}),(0,g.jsx)(p.Z,{mr:1}),(0,g.jsx)(h.ZP,{muted:!P,success:P,children:"Required"})]})]}),(0,g.jsx)(p.Z,{mr:b.cd}),(0,g.jsx)(Y.ZP,{iconOnly:!0,noBackground:!0,noBorder:!0,noPadding:!0,onClick:function(){return ye(o,null)},children:(0,g.jsx)(I.x8,{default:!0})})]})})}),(0,g.jsx)(X.Z,{muted:!0}),(0,g.jsxs)(p.Z,{p:b.cd,children:[(0,g.jsxs)(d.ZP,{fullWidth:!0,children:[(0,g.jsxs)(a.Z,{flex:1,flexDirection:"column",children:[(0,g.jsx)(p.Z,{mb:1,children:(0,g.jsx)(h.ZP,{bold:!0,default:!0,children:"Label"})}),(0,g.jsx)(m.Z,{onChange:function(e){return ye(o,{name:e.target.value})},value:y}),(0,g.jsxs)(p.Z,{mt:b.Mq,children:[(0,g.jsx)(p.Z,{mb:1,children:(0,g.jsx)(h.ZP,{bold:!0,default:!0,children:"Valid data types"})}),(0,g.jsx)(d.ZP,{alignItems:"center",flexWrap:"wrap",children:f.n8.map((function(e){var n=null===E||void 0===E?void 0:E.includes(e);return(0,g.jsx)(p.Z,{mr:b.cd,children:(0,g.jsx)(s.Z,{checked:n,label:(0,z.vg)(e),onClick:function(){return ye(o,{types:n?null===E||void 0===E?void 0:E.filter((function(n){return n!==e})):(E||[]).concat(e)})}})},e)}))})]})]}),(0,g.jsx)(p.Z,{mr:b.Mq}),(0,g.jsxs)(a.Z,{flex:1,flexDirection:"column",children:[(0,g.jsx)(p.Z,{mb:1,children:(0,g.jsx)(h.ZP,{bold:!0,default:!0,children:"Description"})}),(0,g.jsx)(j.Z,{onChange:function(e){return ye(o,{description:e.target.value})},rows:Math.max(3,null===u||void 0===u||null===(t=u.split("\n"))||void 0===t?void 0:t.length),value:u})]})]}),(0,g.jsxs)(p.Z,{mt:b.Mq,children:[(0,g.jsx)(d.ZP,{alignContent:"center",flexDirection:"row",justifyContent:"space-between",children:(0,g.jsxs)(d.ZP,{flexDirection:"column",children:[(0,g.jsx)(h.ZP,{bold:!0,default:!0,children:"Input"}),(0,g.jsx)(h.ZP,{muted:!0,children:"Associate an existing input to this variable or create a new input and then associate it to this variable."})]})}),(0,g.jsx)(p.Z,{mt:1,children:(0,g.jsxs)(v.Z,{monospace:!0,onChange:function(e){var n=e.target.value;"+ Add a new input"===n?(G(!0),oe(o),setTimeout((function(){var e;return null===R||void 0===R||null===(e=R.current)||void 0===e?void 0:e.focus()}),1)):ye(o,{input:n})},placeholder:"Select an existing input",value:Z,children:[(0,g.jsx)("option",{value:""}),(0,g.jsx)("option",{value:"+ Add a new input",children:"+ Add a new input"}),Object.keys(je||{}).map((function(e){return(0,g.jsx)("option",{value:e,children:e},e)}))]})})]})]}),Z&&(0,g.jsxs)(g.Fragment,{children:[(0,g.jsx)(X.Z,{muted:!0}),(0,g.jsxs)(p.Z,{p:b.cd,children:[(0,g.jsx)(p.Z,{mb:1,children:(0,g.jsx)(h.ZP,{muted:!0,rightAligned:!0,small:!0,uppercase:!0,children:"Preview"})}),!(null!==w&&void 0!==w&&w.type)&&(0,g.jsxs)(h.ZP,{muted:!0,children:["Select an input style for ",Z," before seeing a preview."]}),(null===w||void 0===w?void 0:w.type)&&(0,g.jsx)(O,{interaction:{inputs:(0,r.Z)({},Z,null===je||void 0===je?void 0:je[Z]),layout:[[{variable:o,width:1}]],variables:(0,r.Z)({},o,l)}})]})]})]})},"".concat(o,"-").concat(n))}))}),[je,ne,L,oe,ye,be]),Pe=(0,i.useMemo)((function(){return!(null===be||void 0===be||!be[de])}),[de,be]),Ee=(0,i.useMemo)((function(){return!(null===je||void 0===je||!je[ce])}),[je,ce]),we=(0,i.useMemo)((function(){return(0,g.jsx)(q,{containerRef:D,containerWidth:y,interaction:P,showVariableUUID:!0,updateLayout:function(e){return ge({layout:e})}})}),[D,y,P,ge]),De=(0,i.useMemo)((function(){return(0,g.jsxs)(d.ZP,{alignItems:"center",children:[!_&&(0,g.jsx)(Y.ZP,{beforeIcon:(0,g.jsx)(I.mm,{}),compact:!0,onClick:function(e){(0,Q.j)(e),N(!0),setTimeout((function(){var e;return null===M||void 0===M||null===(e=M.current)||void 0===e?void 0:e.focus()}),1)},secondary:!0,small:!0,children:"Add new variable"}),_&&(0,g.jsxs)(g.Fragment,{children:[Pe&&(0,g.jsxs)(g.Fragment,{children:[(0,g.jsx)(h.ZP,{danger:!0,small:!0,children:"Variable already exists"}),(0,g.jsx)(p.Z,{mr:1})]}),(0,g.jsx)(m.Z,{compact:!0,meta:{touched:!!Pe,error:String(Pe)},monospace:!0,onChange:function(e){(0,Q.j)(e),se(e.target.value)},onClick:function(e){return(0,Q.j)(e)},ref:M,small:!0,value:de||""}),(0,g.jsx)(p.Z,{mr:1}),(0,g.jsx)(Y.ZP,{disabled:Pe,compact:!0,onClick:function(e){if((0,Q.j)(e),!Pe){var n=(0,l.Z)(me||[]);n.push([{width:1,variable:de}]),ge($($({},P),{},{layout:n,variables:$($({},be),{},(0,r.Z)({},de,{}))})),N(!1),te(de),se(null),pe({0:!0}),setTimeout((function(){var e;null===L||void 0===L||null===(e=L.current)||void 0===e||e.scrollIntoView(),pe({})}),K.e+100)}},primary:!0,small:!0,children:"Create variable"}),(0,g.jsx)(p.Z,{mr:1}),(0,g.jsx)(Y.ZP,{compact:!0,onClick:function(e){(0,Q.j)(e),N(!1),se(null)},secondary:!0,small:!0,children:"Cancel"})]})]})}),[_,me,de,L,M,N,te,se,pe,ge,Pe,be]),Ce=(0,i.useMemo)((function(){return(0,g.jsxs)(d.ZP,{alignItems:"center",children:[!U&&(0,g.jsx)(Y.ZP,{beforeIcon:(0,g.jsx)(I.mm,{}),compact:!0,onClick:function(e){(0,Q.j)(e),G(!0),setTimeout((function(){var e;return null===R||void 0===R||null===(e=R.current)||void 0===e?void 0:e.focus()}),1)},secondary:!0,small:!0,children:"Add new input"}),U&&(0,g.jsxs)(g.Fragment,{children:[Ee&&(0,g.jsxs)(g.Fragment,{children:[(0,g.jsx)(h.ZP,{danger:!0,small:!0,children:"Input already exists"}),(0,g.jsx)(p.Z,{mr:1})]}),(0,g.jsx)(m.Z,{compact:!0,meta:{touched:!!Ee,error:String(Ee)},monospace:!0,onClick:function(e){return(0,Q.j)(e)},onChange:function(e){(0,Q.j)(e),ue(e.target.value)},ref:R,small:!0,value:ce||""}),(0,g.jsx)(p.Z,{mr:1}),(0,g.jsx)(Y.ZP,{disabled:Ee,compact:!0,onClick:function(e){(0,Q.j)(e),Ee||(ie?ge($($({},P),{},{inputs:$($({},je),{},(0,r.Z)({},ce,{})),variables:$($({},be),{},(0,r.Z)({},ie,$($({},null===be||void 0===be?void 0:be[ie]),{},{input:ce})))})):Ze(ce,{}),G(!1),J(ce),oe(null),ue(null),pe({1:!0}),setTimeout((function(){var e;null===k||void 0===k||null===(e=k.current)||void 0===e||e.scrollIntoView(),pe({})}),K.e+100))},primary:!0,small:!0,children:"Create input"}),(0,g.jsx)(p.Z,{mr:1}),(0,g.jsx)(Y.ZP,{compact:!0,onClick:function(e){(0,Q.j)(e),G(!1),ue(null)},secondary:!0,small:!0,children:"Cancel"})]})]})}),[Ee,je,P,U,ie,ce,k,R,G,J,oe,ue,pe,Ze,be]);return(0,g.jsxs)(C,{ref:D,children:[(0,g.jsx)(S,{children:(0,g.jsx)(p.Z,{p:b.cd,children:(0,g.jsxs)(d.ZP,{alignItems:"center",justifyContent:"space-between",children:[(0,g.jsx)(h.ZP,{default:!0,large:!0,monospace:!0,children:xe}),E&&(0,g.jsxs)(g.Fragment,{children:[(0,g.jsx)(p.Z,{mr:b.cd}),(0,g.jsx)(Y.ZP,{iconOnly:!0,noBackground:!0,noBorder:!0,noPadding:!0,onClick:function(){return E()},children:(0,g.jsx)(I.x8,{default:!0})})]})]})})}),(0,g.jsx)(X.Z,{muted:!0}),Z,(0,g.jsxs)(H.Z,{noBorder:!0,visibleMapping:{0:!0,1:!0,2:!0},visibleMappingForced:ve,children:[(0,g.jsx)(K.Z,{noBorderRadius:!0,noPaddingContent:!0,onClick:function(){pe({})},titleXPadding:b.cd*b.iI,titleYPadding:b.iI,title:(0,g.jsxs)(d.ZP,{alignItems:"center",justifyContent:"space-between",children:[(0,g.jsx)(p.Z,{mr:b.cd,py:1,children:(0,g.jsx)(o.Z,{level:5,children:"Variables"})}),(null===(n=Object.keys(be||{}))||void 0===n?void 0:n.length)>=1&&De]}),children:(0,g.jsxs)(p.Z,{p:b.cd,children:[Ie,!(null!==(t=Object.keys(be||{}))&&void 0!==t&&t.length)&&De]})}),(0,g.jsx)(K.Z,{noBorderRadius:!0,noPaddingContent:!0,onClick:function(){pe({})},titleXPadding:b.cd*b.iI,titleYPadding:b.iI,title:(0,g.jsxs)(d.ZP,{alignItems:"center",justifyContent:"space-between",children:[(0,g.jsx)(p.Z,{mr:b.cd,py:1,children:(0,g.jsx)(o.Z,{level:5,children:"Inputs"})}),(null===(c=Object.keys(je||{}))||void 0===c?void 0:c.length)>=1&&Ce]}),children:(0,g.jsxs)(p.Z,{p:b.cd,children:[Oe,!(null!==(u=Object.keys(je||{}))&&void 0!==u&&u.length)&&Ce]})}),(0,g.jsxs)(K.Z,{noBorderRadius:!0,noPaddingContent:!0,onClick:function(){pe({})},titleXPadding:b.cd*b.iI,titleYPadding:b.iI,title:(0,g.jsx)(d.ZP,{alignItems:"center",justifyContent:"space-between",children:(0,g.jsx)(p.Z,{mr:b.cd,py:1,children:(0,g.jsx)(o.Z,{level:5,children:"Interaction layout"})})}),children:[(0,g.jsx)(p.Z,{p:1,children:we}),!(null!==me&&void 0!==me&&me.length)&&(0,g.jsx)(p.Z,{px:b.cd,pb:b.cd,children:(0,g.jsx)(h.ZP,{muted:!0,children:"Add at least 1 variable and associate an input to it and see a preview."})})]})]})]})};function ne(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function te(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?ne(Object(t),!0).forEach((function(n){(0,r.Z)(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):ne(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}var re=function(e){var n=e.blockInteraction,t=e.children,l=e.contained,c=e.containerRef,u=e.containerWidth,a=e.interaction,d=e.isEditing,s=e.removeBlockInteraction,f=e.setInteractionsMapping,v=e.setVariables,j=e.showVariableUUID,m=e.variables,x=e.widthOffset,Z=(0,i.useMemo)((function(){return n||{description:null,name:null}}),[n]),y=Z.description,O=Z.name,I=(0,i.useCallback)((function(e){return null===f||void 0===f?void 0:f((function(n){return te(te({},n),{},(0,r.Z)({},null===e||void 0===e?void 0:e.uuid,te(te({},a),e)))}))}),[a,f]),P=(0,i.useMemo)((function(){var e;return(0,g.jsxs)(g.Fragment,{children:[O&&(0,g.jsxs)(p.Z,{mb:b.cd,pt:b.cd,px:b.cd,children:[(0,g.jsx)(o.Z,{level:5,children:O}),y&&(null===y||void 0===y||null===(e=y.split("\n"))||void 0===e?void 0:e.map((function(e){return(0,g.jsx)(h.ZP,{default:!0,children:e},e)})))]}),(0,g.jsx)(p.Z,{pb:b.Mq,pt:O?0:b.cd,px:1,children:(0,g.jsx)(q,{containerRef:c,containerWidth:u,interaction:a,setVariables:v,showVariableUUID:j,variables:m,widthOffset:x})})]})}),[y,O,c,u,a,v,j,m,x]);return(0,g.jsxs)("div",{children:[d&&(0,g.jsx)(ee,{containerWidth:u,interaction:a,removeBlockInteraction:s,updateInteraction:I,children:t}),!d&&(0,g.jsxs)(g.Fragment,{children:[l&&P,!l&&(0,g.jsx)(C,{children:P})]})]})}},61599:function(e,n,t){t.d(n,{D5:function(){return m},MU:function(){return l},RL:function(){return a},Xv:function(){return d},Zj:function(){return j},_B:function(){return i},eL:function(){return s},fe:function(){return p},jL:function(){return u},kB:function(){return x},ks:function(){return v},th:function(){return h},u7:function(){return f},zS:function(){return c}});var r,i,o=t(82394);!function(e){e.FULL_TABLE="FULL_TABLE",e.INCREMENTAL="INCREMENTAL",e.LOG_BASED="LOG_BASED"}(i||(i={}));var l,c,u=[i.FULL_TABLE,i.INCREMENTAL];!function(e){e.IGNORE="IGNORE",e.UPDATE="UPDATE"}(l||(l={})),function(e){e.DATE_TIME="date-time",e.UUID="uuid"}(c||(c={}));var a,d="datetime",s=(r={},(0,o.Z)(r,c.DATE_TIME,d),(0,o.Z)(r,c.UUID,c.UUID),r);!function(e){e.ARRAY="array",e.BOOLEAN="boolean",e.INTEGER="integer",e.NULL="null",e.NUMBER="number",e.OBJECT="object",e.STRING="string"}(a||(a={}));var f,v,p,h,j,m=[a.ARRAY,a.BOOLEAN,d,a.INTEGER,a.NULL,a.NUMBER,a.OBJECT,a.STRING,c.UUID];!function(e){e.PROPERTIES="properties"}(f||(f={})),function(e){e.AUTOMATIC="automatic",e.AVAILABLE="available",e.UNSUPPORTED="unsupported"}(v||(v={})),function(e){e.FORCED_REPLICATION_METHOD="forced-replication-method",e.KEY_PROPERTIES="table-key-properties",e.REPLICATION_KEYS="valid-replication-keys",e.SCHEMA_NAME="schema-name"}(p||(p={})),function(e){e.AMPLITUDE="amplitude",e.BIGQUERY="bigquery",e.CHARGEBEE="chargebee",e.GOOGLE_ADS="google_ads",e.GOOGLE_SEARCH_CONSOLE="google_search_console",e.GOOGLE_SHEETS="google_sheets",e.INTERCOM="intercom",e.MYSQL="mysql",e.PIPEDRIVE="pipedrive",e.POSTGRESQL="postgresql",e.REDSHIFT="redshift",e.SALESFORCE="salesforce",e.STRIPE="stripe"}(h||(h={})),function(e){e.AMAZON_S3="amazon_s3",e.BIGQUERY="bigquery",e.DELTA_LAKE_S3="delta_lake_s3",e.GOOGLE_CLOUD_STORAGE="google_cloud_storage",e.KAFKA="kafka",e.MYSQL="mysql",e.POSTGRESQL="postgresql",e.SNOWFLAKE="snowflake"}(j||(j={}));var x=[j.AMAZON_S3,j.GOOGLE_CLOUD_STORAGE,j.KAFKA]},54193:function(e,n,t){var r;t.d(n,{al:function(){return l},bB:function(){return r},n8:function(){return c},qS:function(){return o},zj:function(){return i}}),function(e){e.CHECKBOX="checkbox",e.DROPDOWN_MENU="dropdown_menu",e.SWITCH="switch",e.TEXT_FIELD="text_field"}(r||(r={}));var i,o=[r.CHECKBOX,r.DROPDOWN_MENU,r.SWITCH,r.TEXT_FIELD];!function(e){e.BOOLEAN="boolean",e.DATE="date",e.DATETIME="datetime",e.DICTIONARY="dictionary",e.FLOAT="float",e.INTEGER="integer",e.LIST="list",e.STRING="string"}(i||(i={}));var l,c=[i.BOOLEAN,i.DATE,i.DATETIME,i.DICTIONARY,i.FLOAT,i.INTEGER,i.LIST,i.STRING];!function(e){e.NUMBER="number"}(l||(l={}))},22286:function(e,n,t){t.d(n,{M:function(){return d}});var r=t(82394),i=t(75582),o=t(54193),l=t(81728),c=t(42122);function u(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function a(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?u(Object(t),!0).forEach((function(n){(0,r.Z)(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):u(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}function d(e,n){var t,u;if(!n||null===n||void 0===n||!n.length)return e;if(null!==n&&void 0!==n&&n.includes(o.zj.LIST))return((0,c.Kn)(e)?Object.keys(e||{}):[e]).map((function(e){return d(e,null===n||void 0===n?void 0:n.filter((function(e){return o.zj.LIST!==e})))}));if(null!==n&&void 0!==n&&n.includes(o.zj.DICTIONARY)){var s=(0,c.Kn)(e)?e:(0,l.Pb)(e)?JSON.parse(e):e;if((0,c.Kn)(s))return Object.entries(s).reduce((function(e,t){var l=(0,i.Z)(t,2),c=l[0],u=l[1];return a(a({},e),{},(0,r.Z)({},c,d(u,null===n||void 0===n?void 0:n.filter((function(e){return o.zj.DICTIONARY!==e})))))}),{})}if(null!==n&&void 0!==n&&n.includes(o.zj.BOOLEAN)){var f,v;if("boolean"===typeof e)return e;if("true"===(null===(f=String(e))||void 0===f?void 0:f.toLowerCase()))return!0;if("false"===(null===(v=String(e))||void 0===v?void 0:v.toLowerCase()))return!1}return null!==n&&void 0!==n&&null!==(t=n.includes)&&void 0!==t&&t.call(n,o.zj.FLOAT)&&(0,l.HW)(e)?parseFloat(e):null!==n&&void 0!==n&&null!==(u=n.includes)&&void 0!==u&&u.call(n,o.zj.INTEGER)&&(0,l.HW)(e)?parseInt(e):e}}}]);