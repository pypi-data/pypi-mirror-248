(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[4085],{34331:function(e,n,i){"use strict";i.r(n);var t=i(77837),r=i(38860),s=i.n(r),u=i(82684),c=i(34376),o=i(71180),d=i(15338),l=i(55485),a=i(58146),p=i(93808),m=i(28274),f=i(38276),h=i(75499),v=i(30160),x=i(35686),j=i(72473),_=i(70515),P=i(24755),Z=i(3917),w=i(36717),b=i(28598);function k(){var e=(0,c.useRouter)(),n=(0,u.useState)(!1),i=n[0],t=n[1],r=x.ZP.permissions.list({_limit:1e3}).data,s=(0,u.useMemo)((function(){return(null===r||void 0===r?void 0:r.permissions)||[]}),[r]),p=[{bold:!i,label:function(){return"Permissions"}}];return i?(p[0].onClick=function(){return t(!1)},p.push({bold:!0,label:function(){return"New permission"}})):p[0].linkProps={href:"/settings/workspace/permissions"},(0,b.jsxs)(m.Z,{appendBreadcrumbs:!0,breadcrumbs:p,title:"Permissions",uuidItemSelected:P.B2.PERMISSIONS,uuidWorkspaceSelected:P.Pl.USER_MANAGEMENT,children:[i&&(0,b.jsx)(a.Z,{contained:!0,onCancel:function(){return t(!1)}}),!i&&(0,b.jsxs)(b.Fragment,{children:[(0,b.jsx)(f.Z,{p:_.cd,children:(0,b.jsx)(o.ZP,{beforeIcon:(0,b.jsx)(j.QM,{}),onClick:function(){return t(!0)},primary:!0,children:"Add new permission"})}),(0,b.jsx)(d.Z,{light:!0}),(0,b.jsx)(h.Z,{columnFlex:[3,1,null,6,null,null],columns:[{uuid:"Entity"},{uuid:"Subtype"},{uuid:"Entity ID"},{uuid:"Access"},{uuid:"Last updated"},{rightAligned:!0,uuid:"Created at"}],onClickRow:function(n){var i,t=null===(i=s[n])||void 0===i?void 0:i.id;e.push("/settings/workspace/permissions/".concat(t))},rows:null===s||void 0===s?void 0:s.map((function(e){var n=e.access,i=e.created_at,t=e.entity,r=e.entity_id,s=e.entity_name,u=e.entity_type,c=(e.id,e.updated_at),o=(e.user,n?(0,w.q)(n):[]),d=(null===o||void 0===o?void 0:o.length)||0;return[(0,b.jsx)(v.ZP,{monospace:!0,children:s||t},"entityName"),(0,b.jsx)(v.ZP,{default:!0,monospace:!!u,children:u||"-"},"entityType"),(0,b.jsx)(v.ZP,{default:!0,monospace:!!r,children:r||"-"},"entityID"),(0,b.jsx)("div",{children:d>=1&&(0,b.jsx)(l.ZP,{alignItems:"center",flexWrap:"wrap",children:null===o||void 0===o?void 0:o.map((function(e,n){return(0,b.jsx)("div",{children:(0,b.jsxs)(v.ZP,{default:!0,monospace:!0,small:!0,children:[e,d>=2&&n<d-1&&(0,b.jsx)(v.ZP,{inline:!0,muted:!0,small:!0,children:",\xa0"})]})},e)}))})},"access"),(0,b.jsx)(v.ZP,{monospace:!0,default:!0,children:c&&(0,Z.d$)(c)},"updatedAt"),(0,b.jsx)(v.ZP,{monospace:!0,default:!0,rightAligned:!0,children:i&&(0,Z.d$)(i)},"createdAt")]})),uuid:"permissions"})]})]})}k.getInitialProps=(0,t.Z)(s().mark((function e(){return s().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.abrupt("return",{});case 1:case"end":return e.stop()}}),e)}))),n.default=(0,p.Z)(k)},36717:function(e,n,i){"use strict";i.d(n,{q:function(){return s}});var t=i(75582),r=i(36288);function s(e){return Object.entries(r.K4).reduce((function(n,i){var r=(0,t.Z)(i,2),s=r[0],u=r[1];return e&Number(s)?n.concat(u):n}),[])}},65960:function(e,n,i){(window.__NEXT_P=window.__NEXT_P||[]).push(["/settings/workspace/permissions",function(){return i(34331)}])}},function(e){e.O(0,[2678,1154,844,874,1557,8264,7858,5499,8432,8146,9774,2888,179],(function(){return n=65960,e(e.s=n);var n}));var n=e.O();_N_E=n}]);