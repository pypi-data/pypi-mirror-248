(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[6308],{65956:function(n,e,t){"use strict";var i=t(38626),o=t(55485),r=t(38276),c=t(30160),a=t(44897),l=t(42631),d=t(47041),u=t(70515),s=t(28598),h=(0,i.css)(["padding:","px;padding-bottom:","px;padding-top:","px;"],2*u.iI,1.5*u.iI,1.5*u.iI),f=i.default.div.withConfig({displayName:"Panel__PanelStyle",componentId:"sc-1ct8cgl-0"})(["border-radius:","px;overflow:hidden;"," "," "," "," "," "," "," "," "," "," "," ",""],l.n_,(function(n){return n.fullWidth&&"\n    width: 100%;\n  "}),(function(n){return!n.borderless&&"\n    border: 1px solid ".concat((n.theme.interactive||a.Z.interactive).defaultBorder,";\n  ")}),(function(n){return n.success&&"\n    background-color: ".concat((n.theme.background||a.Z.background).successLight,";\n  ")}),(function(n){return n.success&&!n.borderless&&"\n    border: 1px solid ".concat((n.theme.background||a.Z.background).success,";\n  ")}),(function(n){return!n.dark&&!n.success&&"\n    background-color: ".concat((n.theme.background||a.Z.background).panel,";\n  ")}),(function(n){return n.dark&&"\n    background-color: ".concat((n.theme.background||a.Z.background).content,";\n  ")}),(function(n){return!n.fullHeight&&"\n    height: fit-content;\n  "}),(function(n){return n.maxHeight&&"\n    max-height: ".concat(n.maxHeight,";\n  ")}),(function(n){return n.maxWidth&&"\n    max-width: ".concat(n.maxWidth,"px;\n  ")}),(function(n){return n.minWidth&&"\n    min-width: ".concat(n.minWidth,"px;\n\n    @media (max-width: ").concat(n.minWidth,"px) {\n      min-width: 0;\n    }\n  ")}),(function(n){return n.borderless&&"\n    border: none;\n  "}),(function(n){return n.overflowVisible&&"\n    overflow: visible;\n  "})),p=i.default.div.withConfig({displayName:"Panel__HeaderStyle",componentId:"sc-1ct8cgl-1"})(["border-top-left-radius:","px;border-top-right-radius:","px;"," "," "," ",""],l.n_,l.n_,(function(n){return"\n    background-color: ".concat((n.theme.background||a.Z.background).chartBlock,";\n    border-bottom: 1px solid ").concat((n.theme.interactive||a.Z.interactive).defaultBorder,";\n  ")}),(function(n){return n.height&&"\n    height: ".concat(n.height,"px;\n  ")}),h,(function(n){return n.headerPaddingVertical&&"\n    padding-bottom: ".concat(n.headerPaddingVertical,"px;\n    padding-top: ").concat(n.headerPaddingVertical,"px;\n  ")})),m=i.default.div.withConfig({displayName:"Panel__ContentStyle",componentId:"sc-1ct8cgl-2"})(["overflow-y:auto;padding:","px;height:100%;"," "," "," "," ",""],1.75*u.iI,d.w5,(function(n){return n.height&&"\n    height: ".concat(n.height,"px;\n  ")}),(function(n){return n.maxHeight&&"\n    max-height: calc(".concat(n.maxHeight," - ").concat(15*u.iI,"px);\n  ")}),(function(n){return n.noPadding&&"\n    padding: 0;\n  "}),(function(n){return n.overflowVisible&&"\n    overflow: visible;\n  "})),g=i.default.div.withConfig({displayName:"Panel__FooterStyle",componentId:"sc-1ct8cgl-3"})(["border-style:",";border-top-width:","px;padding:","px;"],l.M8,l.YF,1.75*u.iI);e.Z=function(n){var e=n.borderless,t=n.children,i=n.containerRef,a=n.contentContainerRef,l=n.dark,d=n.footer,u=n.fullHeight,h=void 0===u||u,x=n.fullWidth,b=void 0===x||x,y=n.header,w=n.headerHeight,v=n.headerIcon,_=n.headerPaddingVertical,j=n.headerTitle,I=n.maxHeight,Z=n.maxWidth,N=n.minWidth,H=n.noPadding,P=n.overflowVisible,k=n.subtitle,S=n.success;return(0,s.jsxs)(f,{borderless:e,dark:l,fullHeight:h,fullWidth:b,maxHeight:I,maxWidth:Z,minWidth:N,overflowVisible:P,ref:i,success:S,children:[(y||j)&&(0,s.jsxs)(p,{headerPaddingVertical:_,height:w,children:[y&&y,j&&(0,s.jsx)(o.ZP,{alignItems:"center",justifyContent:"space-between",children:(0,s.jsxs)(o.ZP,{alignItems:"center",children:[v&&v,(0,s.jsx)(r.Z,{ml:v?1:0,children:(0,s.jsx)(c.ZP,{bold:!0,default:!0,children:j})})]})})]}),(0,s.jsxs)(m,{maxHeight:I,noPadding:H,overflowVisible:P,ref:a,children:[k&&"string"===typeof k&&(0,s.jsx)(r.Z,{mb:2,children:(0,s.jsx)(c.ZP,{default:!0,children:k})}),k&&"string"!==typeof k&&k,t]}),d&&(0,s.jsx)(g,{children:d})]})}},85854:function(n,e,t){"use strict";var i,o,r,c,a,l,d,u,s=t(82394),h=t(26304),f=t(26653),p=t(38626),m=t(33591),g=t(44897),x=t(95363),b=t(61896),y=t(30160),w=t(70515),v=t(38276),_=t(28598),j=["children","condensed","inline","level","marketing","spacingBelow"];function I(n,e){var t=Object.keys(n);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(n);e&&(i=i.filter((function(e){return Object.getOwnPropertyDescriptor(n,e).enumerable}))),t.push.apply(t,i)}return t}function Z(n){for(var e=1;e<arguments.length;e++){var t=null!=arguments[e]?arguments[e]:{};e%2?I(Object(t),!0).forEach((function(e){(0,s.Z)(n,e,t[e])})):Object.getOwnPropertyDescriptors?Object.defineProperties(n,Object.getOwnPropertyDescriptors(t)):I(Object(t)).forEach((function(e){Object.defineProperty(n,e,Object.getOwnPropertyDescriptor(t,e))}))}return n}var N=(0,p.css)([""," margin:0;"," "," "," "," "," "," "," "," "," "," "," "," "," ",""],y.IH,(function(n){return n.color&&"\n    color: ".concat(n.color,"\n  ")}),(function(n){return n.yellow&&"\n    color: ".concat((n.theme.accent||g.Z.accent).yellow,";\n  ")}),(function(n){return n.center&&"\n    text-align: center;\n  "}),(function(n){return!n.monospace&&0===Number(n.weightStyle)&&"\n    font-family: ".concat(x.iI,";\n  ")}),(function(n){return!n.monospace&&1===Number(n.weightStyle)&&"\n    font-family: ".concat(x.LX,";\n  ")}),(function(n){return!n.monospace&&2===Number(n.weightStyle)&&"\n    font-family: ".concat(x.LX,";\n  ")}),(function(n){return!n.monospace&&3===Number(n.weightStyle)&&"\n    font-family: ".concat(x.ry,";\n  ")}),(function(n){return!n.monospace&&4===Number(n.weightStyle)&&"\n    font-family: ".concat(x.YC,";\n  ")}),(function(n){return!n.monospace&&5===Number(n.weightStyle)&&"\n    font-family: ".concat(x.nF,";\n  ")}),(function(n){return!n.monospace&&(6===Number(n.weightStyle)||n.bold)&&"\n    font-family: ".concat(x.nF,";\n  ")}),(function(n){return!n.monospace&&7===Number(n.weightStyle)&&"\n    font-family: ".concat(x.nF,";\n  ")}),(function(n){return!n.monospace&&8===Number(n.weightStyle)&&"\n    font-family: ".concat(x.nF,";\n  ")}),(function(n){return n.lineHeightAuto&&"\n    line-height: normal !important;\n  "}),(function(n){return n.strikethrough&&"\n    text-decoration: line-through;\n  "})),H=p.default.div.withConfig({displayName:"Headline__HeadlineContainerStyle",componentId:"sc-12jzt2e-0"})(["",""],(function(n){return"\n    color: ".concat((n.theme.content||g.Z.content).active,";\n  ")})),P=p.default.h1.withConfig({displayName:"Headline__H1HeroStyle",componentId:"sc-12jzt2e-1"})([""," font-size:42px;line-height:56px;"," "," ",""],N,m.media.md(i||(i=(0,f.Z)(["\n    ","\n  "])),b.aQ),m.media.lg(o||(o=(0,f.Z)(["\n    ","\n  "])),b.aQ),m.media.xl(r||(r=(0,f.Z)(["\n    ","\n  "])),b.aQ)),k=p.default.h1.withConfig({displayName:"Headline__H1Style",componentId:"sc-12jzt2e-2"})([""," ",""],N,b.MJ),S=p.default.h1.withConfig({displayName:"Headline__H1MarketingStyle",componentId:"sc-12jzt2e-3"})([""," "," "," "," "," ",""],N,m.media.xs(c||(c=(0,f.Z)(["\n    font-size: ","px;\n    line-height: ","px;\n  "])),6*w.iI,7*w.iI),m.media.sm(a||(a=(0,f.Z)(["\n    font-size: ","px;\n    line-height: ","px;\n  "])),6*w.iI,7*w.iI),m.media.md(l||(l=(0,f.Z)(["\n    font-size: ","px;\n    line-height: ","px;\n  "])),6*w.iI,7*w.iI),m.media.lg(d||(d=(0,f.Z)(["\n    font-size: ","px;\n    line-height: ","px;\n  "])),6*w.iI,7*w.iI),m.media.xl(u||(u=(0,f.Z)(["\n    font-size: ","px;\n    line-height: ","px;\n  "])),6*w.iI,7*w.iI)),C=p.default.h2.withConfig({displayName:"Headline__H2Style",componentId:"sc-12jzt2e-4"})([""," ",""],N,b.BL),z=p.default.h3.withConfig({displayName:"Headline__H3Style",componentId:"sc-12jzt2e-5"})([""," font-size:24px;line-height:32px;"],N),O=p.default.h4.withConfig({displayName:"Headline__H4Style",componentId:"sc-12jzt2e-6"})([""," font-size:20px;line-height:28px;"],N),W=p.default.h5.withConfig({displayName:"Headline__H5Style",componentId:"sc-12jzt2e-7"})([""," font-size:18px;line-height:26px;"],N),V=p.default.span.withConfig({displayName:"Headline__SpanStyle",componentId:"sc-12jzt2e-8"})([""," "," "," "," ",""],N,(function(n){return 1===n.level&&"\n    ".concat(b.MJ,"\n  ")}),(function(n){return 2===n.level&&"\n    ".concat(b.BL,"\n  ")}),(function(n){return 3===n.level&&"\n    font-size: 24px;\n    line-height: 32px;\n  "}),(function(n){return 4===n.level&&"\n    font-size: 20px;\n    line-height: 28px;\n  "})),B=function(n){var e,t=n.children,i=n.condensed,o=n.inline,r=n.level,c=n.marketing,a=n.spacingBelow,l=(0,h.Z)(n,j);o?e=V:0===Number(r)?e=P:1===Number(r)?e=c?S:k:2===Number(r)?e=C:3===Number(r)?e=z:4===Number(r)?e=O:5===Number(r)&&(e=W);var d=(0,_.jsxs)(e,Z(Z({},l),{},{level:r,children:[a&&(0,_.jsx)(v.Z,{mb:i?2:3,children:t}),!a&&t]}));return o?d:(0,_.jsx)(H,{children:d})};B.defaultProps={level:3,weightStyle:6},e.Z=B},86627:function(n,e,t){"use strict";t.r(e);var i=t(77837),o=t(38860),r=t.n(o),c=t(65956),a=t(93808),l=t(28274),d=t(38276),u=t(36043),s=t(35686),h=t(70515),f=t(24755),p=t(50178),m=t(28598);function g(){var n=((0,p.PR)()||{}).id,e=s.ZP.users.detail(n),t=e.data,i=e.mutate,o=null===t||void 0===t?void 0:t.user;return(0,m.jsx)(l.Z,{uuidItemSelected:f.DQ,uuidWorkspaceSelected:f.tC,children:(0,m.jsx)(d.Z,{p:h.cd,children:(0,m.jsx)(c.Z,{children:(0,m.jsx)(u.Z,{disabledFields:["roles"],onSaveSuccess:i,user:o})})})})}g.getInitialProps=(0,i.Z)(r().mark((function n(){return r().wrap((function(n){for(;;)switch(n.prev=n.next){case 0:return n.abrupt("return",{});case 1:case"end":return n.stop()}}),n)}))),e.default=(0,a.Z)(g)},10736:function(n,e,t){(window.__NEXT_P=window.__NEXT_P||[]).push(["/settings/account/profile",function(){return t(86627)}])}},function(n){n.O(0,[2678,1154,844,874,1557,8264,8432,6043,9774,2888,179],(function(){return e=10736,n(n.s=e);var e}));var e=n.O();_N_E=e}]);