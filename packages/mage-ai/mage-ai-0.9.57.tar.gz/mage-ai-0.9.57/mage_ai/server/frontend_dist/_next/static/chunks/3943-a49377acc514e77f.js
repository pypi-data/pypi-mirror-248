"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[3943],{4611:function(e,n,t){t.d(n,{f:function(){return o}});var i=t(38626),r=t(44897),u=t(70515),l=t(42631),o=i.default.div.withConfig({displayName:"Tablestyle__PopupContainerStyle",componentId:"sc-8ammqd-0"})(["position:absolute;max-height:","px;z-index:10;border-radius:","px;padding:","px;"," "," "," ",""],58*u.iI,l.TR,2*u.iI,(function(e){return"\n    box-shadow: ".concat((e.theme.shadow||r.Z.shadow).popup,";\n    background-color: ").concat((e.theme.interactive||r.Z.interactive).defaultBackground,";\n  ")}),(function(e){return e.leftOffset&&"\n    left: ".concat(e.leftOffset,"px;\n  ")}),(function(e){return e.topOffset&&"\n    top: ".concat(e.topOffset,"px;\n  ")}),(function(e){return e.width&&"\n    width: ".concat(e.width,"px;\n  ")}))},53943:function(e,n,t){var i=t(82394),r=t(75582),u=t(12691),l=t.n(u),o=t(69864),c=t(82684),a=t(34376),s=t(71180),d=t(70652),p=t(50724),f=t(97618),h=t(55485),m=t(48670),v=t(44265),g=t(89515),x=t(38276),_=t(4190),b=t(75499),j=t(48381),E=t(30160),P=t(35686),I=t(44897),Z=t(42631),y=t(72473),O=t(81655),C=t(72191),w=t(39643),k=t(4611),N=t(30229),D=t(31608),T=t(70515),L=t(16488),A=t(86735),R=t(50178),S=t(72619),U=t(95924),V=t(69419),F=t(70320),M=t(3917),Y=t(44688),B=t(28598);function H(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);n&&(i=i.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,i)}return t}function z(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?H(Object(t),!0).forEach((function(n){(0,i.Z)(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):H(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}var G={monospace:!0,small:!0};function K(e){var n=e.cancelingRunId,t=e.disabled,i=e.isLoadingCancelPipeline,u=e.onCancel,l=e.onSuccess,a=e.pipelineRun,d=e.setCancelingRunId,f=e.setErrors,m=e.setShowConfirmationId,g=e.showConfirmationId,b=(0,R.Ct)(),j=a||{},O=j.id,w=j.pipeline_schedule_id,D=j.pipeline_schedule_token,T=j.pipeline_schedule_type,L=j.status,A=i&&O===n&&v.VO.RUNNING===L,U=(0,V.iV)(),F=(0,c.useMemo)((function(){return(null!==U&&void 0!==U&&U.page?+U.page:0)>0}),[null===U||void 0===U?void 0:U.page]),M=(0,o.Db)(N.Xm.API===T&&D?P.ZP.pipeline_runs.pipeline_schedules.useCreateWithParent(w,D):P.ZP.pipeline_runs.pipeline_schedules.useCreate(w),{onSuccess:function(e){return(0,S.wD)(e,{callback:function(){l()},onErrorCallback:function(e,n){return null===f||void 0===f?void 0:f({errors:n,response:e})}})}}),Y=(0,r.Z)(M,1)[0],H=(0,c.useCallback)((function(){m(null),Y({pipeline_run:{backfill_id:null===a||void 0===a?void 0:a.backfill_id,event_variables:(null===a||void 0===a?void 0:a.event_variables)||{},execution_date:null===a||void 0===a?void 0:a.execution_date,pipeline_schedule_id:null===a||void 0===a?void 0:a.pipeline_schedule_id,pipeline_uuid:null===a||void 0===a?void 0:a.pipeline_uuid,variables:(null===a||void 0===a?void 0:a.variables)||{}}})}),[Y,a,m]),z=(0,c.useCallback)((function(){m(null),d(O),u({id:O,status:v.VO.CANCELLED})}),[u,O,d,m]);return(0,B.jsxs)("div",{style:{position:"relative"},children:[(0,B.jsx)(s.ZP,{backgroundColor:A&&I.Z.accent.yellow,beforeIcon:v.VO.INITIAL!==L&&!t&&(0,B.jsxs)(B.Fragment,{children:[v.VO.COMPLETED===L&&(0,B.jsx)(y.Jr,{size:C.bL}),[v.VO.FAILED,v.VO.CANCELLED].includes(L)&&(0,B.jsx)(y.Py,{inverted:v.VO.CANCELLED===L&&!b,size:C.bL}),[v.VO.RUNNING].includes(L)&&(0,B.jsx)(_.Z,{color:A?I.Z.status.negative:I.Z.monotone.white,small:!0})]}),borderRadius:"".concat(Z.D7,"px"),danger:v.VO.FAILED===L&&!b,default:v.VO.INITIAL===L,disabled:t||b,loading:!a,onClick:function(e){e.stopPropagation(),m(O)},padding:"6px",primary:v.VO.RUNNING===L&&!A&&!b,warning:v.VO.CANCELLED===L&&!b,children:t?"Ready":A?"Canceling":v.Do[L]}),(0,B.jsx)(p.Z,{onClickOutside:function(){return m(null)},open:g===O,children:(0,B.jsxs)(k.f,{children:[[v.VO.RUNNING,v.VO.INITIAL].includes(L)&&(0,B.jsxs)(B.Fragment,{children:[(0,B.jsx)(E.ZP,{bold:!0,color:"#9ECBFF",children:"Run is in progress"}),(0,B.jsx)(x.Z,{mb:1}),(0,B.jsxs)(E.ZP,{children:["This pipeline run is currently ongoing. Retrying will cancel",(0,B.jsx)("br",{}),"the current pipeline run."]}),(0,B.jsx)(E.ZP,{}),(0,B.jsx)(x.Z,{mt:1,children:(0,B.jsxs)(h.ZP,{children:[(0,B.jsx)(s.ZP,{onClick:function(){z(),H()},children:"Retry run"}),(0,B.jsx)(x.Z,{ml:1}),(0,B.jsx)(s.ZP,{onClick:z,children:"Cancel run"})]})})]}),[v.VO.CANCELLED,v.VO.FAILED,v.VO.COMPLETED].includes(L)&&(0,B.jsxs)(B.Fragment,{children:[(0,B.jsxs)(E.ZP,{bold:!0,color:"#9ECBFF",children:["Run ",L]}),(0,B.jsx)(x.Z,{mb:1}),(0,B.jsxs)(E.ZP,{children:["Retry the run with changes you have made to the pipeline.",F?(0,B.jsxs)(B.Fragment,{children:[(0,B.jsx)("br",{}),"Note that the retried run may appear on a previous page."]}):null]}),(0,B.jsx)(x.Z,{mb:1}),(0,B.jsx)(s.ZP,{onClick:H,children:"Retry run"})]})]})})]})}n.Z=function(e){var n=e.allowBulkSelect,t=e.allowDelete,u=e.deletePipelineRun,_=e.disableKeyboardNav,I=e.disableRowSelect,k=e.emptyMessage,N=void 0===k?"No runs available":k,V=e.fetchPipelineRuns,H=e.hideTriggerColumn,X=e.includePipelineTags,Q=e.onClickRow,W=e.pipelineRuns,q=e.selectedRun,J=e.selectedRuns,$=e.setSelectedRun,ee=e.setSelectedRuns,ne=e.setErrors,te=(0,a.useRouter)(),ie=(0,R.Ct)(),re=(0,F.qB)(),ue=(0,c.useRef)({}),le=(0,c.useState)(null),oe=le[0],ce=le[1],ae=(0,c.useState)(null),se=ae[0],de=ae[1],pe=(0,c.useState)(null),fe=pe[0],he=pe[1],me=(0,c.useState)(0),ve=me[0],ge=me[1],xe=(0,c.useState)(0),_e=xe[0],be=xe[1],je=(0,o.Db)((function(e){var n=e.id,t=e.status;return P.ZP.pipeline_runs.useUpdate(n)({pipeline_run:{status:t}})}),{onSuccess:function(e){return(0,S.wD)(e,{callback:function(){ce(null),null===V||void 0===V||V()},onErrorCallback:function(e,n){ce(null),null===ne||void 0===ne||ne({errors:n,response:e})}})}}),Ee=(0,r.Z)(je,2),Pe=Ee[0],Ie=Ee[1].isLoading,Ze="PipelineDetail/Runs/Table",ye="pipeline-runs",Oe=(0,c.useCallback)((function(e){if(!e)return null;var n=W.findIndex((function(n){return n.id===e.id}));return n>=0?n:null}),[W]),Ce=(0,Y.y)(),we=Ce.registerOnKeyDown,ke=Ce.unregisterOnKeyDown;(0,c.useEffect)((function(){return function(){ke(Ze)}}),[ke,Ze]),we(Ze,(function(e,n){var t=n[w.Bu],i=n[w.kD];$&&!_&&(t||i)&&$((function(n){var r=Oe(n);if(null!==r){if(e.repeat)return e.preventDefault(),n;if(t){var u=r-1;return u<0&&(u=W.length-1),W[u]}if(i){var l=r+1;return l>=W.length&&(l=0),W[l]}}return n}))}),[W,$]),(0,c.useEffect)((function(){var e=Oe(q);if(null!==e){var n=(0,O.w4)({rowIndex:e,uuid:ye}),t=document.getElementById(n);t&&t.scrollIntoView({behavior:"smooth",block:"center"})}}),[Oe,q]);var Ne=re?O.O$:{},De=[null,null,1],Te=[{uuid:"Status"},{center:!0,uuid:"ID"},{uuid:"Pipeline"}];H||(De.push(1),Te.push({uuid:"Trigger"})),X&&(De.push(null),Te.push({uuid:"Pipeline tags"})),De.push.apply(De,[1,1,1,null,null]),Te.push.apply(Te,[z(z({},Ne),{},{uuid:"Execution date"}),z(z({},Ne),{},{uuid:"Started at"}),z(z({},Ne),{},{uuid:"Completed at"}),{uuid:"Execution time"},{uuid:"Block runs"},{uuid:"Logs"}]),t&&!ie&&(De.push.apply(De,[null]),Te.push({label:function(){return""},uuid:"Delete"}));var Le=(0,c.useMemo)((function(){return W.every((function(e){var n=e.id;return!(null===J||void 0===J||!J[n])}))}),[W,J]);n&&(De.unshift(null),Te.unshift({label:function(){return(0,B.jsx)(d.Z,{checked:Le,onClick:function(){var e=(0,A.HK)(W||[],(function(e){return e.id}));ee(Le?{}:e)}})},uuid:"Selected"})),!I&&Q&&(De.push(null),Te.push({label:function(){return""},uuid:"action"}));var Ae=(0,c.useCallback)((function(e,n){if(Q&&ee&&n&&n.metaKey){var t=W[e];ee((function(e){var n=!(null===e||void 0===e||!e[t.id]);return z(z({},e),{},(0,i.Z)({},t.id,n?null:t))}))}else Q&&Q(e)}),[Q,W,ee]);return(0,B.jsx)(D.cl,{minHeight:30*T.iI,overflowVisible:!!se,children:0===(null===W||void 0===W?void 0:W.length)?(0,B.jsx)(x.Z,{px:3,py:1,children:(0,B.jsx)(E.ZP,{bold:!0,default:!0,monospace:!0,muted:!0,children:N})}):(0,B.jsx)(b.Z,{columnFlex:De,columns:Te,isSelectedRow:function(e){return!I&&W[e].id===(null===q||void 0===q?void 0:q.id)},onClickRow:I?null:Ae,rowVerticalPadding:6,rows:null===W||void 0===W?void 0:W.map((function(e,r){var o=e.block_runs_count,a=e.completed_block_runs_count,_=e.completed_at,b=e.execution_date,P=e.id,w=e.pipeline_schedule_id,k=e.pipeline_schedule_name,N=e.pipeline_tags,D=e.pipeline_uuid,T=e.started_at,A=e.status;ue.current[P]=(0,c.createRef)();var R,S,F=!P&&!A,Y="".concat(a," out of ").concat(o," block runs completed"),q=(0,B.jsx)(j.Z,{tags:null===N||void 0===N?void 0:N.map((function(e){return{uuid:e}}))},"row_pipeline_tags_".concat(r)),$=[];r>0&&W[r-1].execution_date===e.execution_date&&W[r-1].pipeline_schedule_id===e.pipeline_schedule_id?($=[(0,B.jsx)(x.Z,{ml:1,children:(0,B.jsxs)(h.ZP,{alignItems:"center",children:[(0,B.jsx)(y.TT,{size:C.bL,useStroke:!0}),(0,B.jsx)(s.ZP,{borderRadius:"".concat(Z.D7,"px"),notClickable:!0,padding:"6px",children:(0,B.jsx)(E.ZP,{muted:!0,children:v.Do[A]})})]})},"row_status"),(0,B.jsx)(E.ZP,{center:!0,default:!0,monospace:!0,muted:!0,children:null===e||void 0===e?void 0:e.id},"row_id"),(0,B.jsx)(E.ZP,{default:!0,monospace:!0,muted:!0,children:D},"row_pipeline_uuid")],H||$.push((0,B.jsx)(E.ZP,{default:!0,monospace:!0,muted:!0,children:"-"},"row_trigger_retry")),X&&$.push(q),(R=$).push.apply(R,[(0,B.jsx)(E.ZP,{default:!0,monospace:!0,muted:!0,children:"-"},"row_date_retry"),(0,c.createElement)(E.ZP,z(z({},G),{},{key:"row_started_at",muted:!0,title:T?(0,M._6)(T):null}),T?(0,L.Uc)(T,re):(0,B.jsx)(B.Fragment,{children:"\u2014"})),(0,c.createElement)(E.ZP,z(z({},G),{},{key:"row_completed_at",muted:!0,title:_?(0,M._6)(_):null}),_?(0,L.Uc)(_,re):(0,B.jsx)(B.Fragment,{children:"\u2014"})),(0,c.createElement)(E.ZP,z(z({},G),{},{default:!0,key:"row_execution_time",title:T&&_?(0,M.Qf)({endDatetime:_,showFullFormat:!0,startDatetime:T}):null}),T&&_?(0,M.Qf)({endDatetime:_,startDatetime:T}):(0,B.jsx)(B.Fragment,{children:"\u2014"})),(0,B.jsx)(l(),{as:"/pipelines/".concat(D,"/runs/").concat(P),href:"/pipelines/[pipeline]/runs/[run]",passHref:!0,children:(0,B.jsx)(m.Z,{bold:!0,muted:!0,title:Y,children:"".concat(a," / ").concat(o)})},"row_block_runs"),(0,B.jsx)(s.ZP,{default:!0,iconOnly:!0,noBackground:!0,onClick:function(e){e.stopPropagation(),te.push("/pipelines/".concat(D,"/logs?pipeline_run_id[]=").concat(P))},children:(0,B.jsx)(y.UL,{default:!0,size:C.bL})},"row_logs")])):($=[(0,B.jsx)(K,{cancelingRunId:oe,disabled:F,isLoadingCancelPipeline:Ie,onCancel:Pe,onSuccess:V,pipelineRun:e,setCancelingRunId:ce,setErrors:ne,setShowConfirmationId:de,showConfirmationId:se},"row_retry_button"),(0,B.jsx)(E.ZP,{center:!0,default:!0,monospace:!0,muted:!0,children:null===e||void 0===e?void 0:e.id},"row_id"),(0,B.jsx)(E.ZP,{default:!0,monospace:!0,children:D},"row_pipeline_uuid")],H||$.push((0,B.jsx)(l(),{as:"/pipelines/".concat(D,"/triggers/").concat(w),href:"/pipelines/[pipeline]/triggers/[...slug]",passHref:!0,children:(0,B.jsx)(m.Z,{bold:!0,sky:!0,children:k})},"row_trigger")),X&&$.push(q),(S=$).push.apply(S,[(0,c.createElement)(E.ZP,z(z({},G),{},{default:!0,key:"row_date",title:b?(0,M._6)(b):null}),b?(0,L.Uc)(b,re):(0,B.jsx)(B.Fragment,{children:"\u2014"})),(0,c.createElement)(E.ZP,z(z({},G),{},{default:!0,key:"row_started_at",title:T?(0,M._6)(T):null}),T?(0,L.Uc)(T,re):(0,B.jsx)(B.Fragment,{children:"\u2014"})),(0,c.createElement)(E.ZP,z(z({},G),{},{default:!0,key:"row_completed_at",title:_?(0,M._6)(_):null}),_?(0,L.Uc)(_,re):(0,B.jsx)(B.Fragment,{children:"\u2014"})),(0,c.createElement)(E.ZP,z(z({},G),{},{default:!0,key:"row_execution_time",title:T&&_?(0,M.Qf)({endDatetime:_,showFullFormat:!0,startDatetime:T}):null}),T&&_?(0,M.Qf)({endDatetime:_,startDatetime:T}):(0,B.jsx)(B.Fragment,{children:"\u2014"})),(0,B.jsx)(l(),{as:"/pipelines/".concat(D,"/runs/").concat(P),href:"/pipelines/[pipeline]/runs/[run]",passHref:!0,children:(0,B.jsx)(m.Z,{bold:!0,disabled:F,sky:!0,title:Y,children:F?"":"".concat(a," / ").concat(o)})},"row_block_runs"),(0,B.jsx)(s.ZP,{default:!0,disabled:F,iconOnly:!0,noBackground:!0,onClick:function(e){e.stopPropagation(),te.push("/pipelines/".concat(D,"/logs?pipeline_run_id[]=").concat(P))},children:(0,B.jsx)(y.UL,{default:!0,size:C.bL})},"row_logs")]));if(t&&!ie&&$.push((0,B.jsxs)(B.Fragment,{children:[(0,B.jsx)(s.ZP,{default:!0,iconOnly:!0,noBackground:!0,onClick:function(e){var n,t,i,r;(0,U.j)(e),he(P),ge((null===(n=ue.current[P])||void 0===n||null===(t=n.current)||void 0===t?void 0:t.offsetTop)||0),be((null===(i=ue.current[P])||void 0===i||null===(r=i.current)||void 0===r?void 0:r.offsetLeft)||0)},ref:ue.current[P],title:"Delete",children:(0,B.jsx)(y.rF,{default:!0,size:C.bL})}),(0,B.jsx)(p.Z,{onClickOutside:function(){return he(null)},open:fe===P,children:(0,B.jsx)(g.Z,{danger:!0,left:(_e||0)-O.nH,onCancel:function(){return he(null)},onClick:function(){he(null),u(P)},title:"Are you sure you want to delete this run (id ".concat(P,' for trigger "').concat(k,'")?'),top:(ve||0)-(r<=1?O.oz:O.OK),width:O.Xx})})]})),n){var le=!(null===J||void 0===J||!J[P]);$.unshift((0,B.jsx)(d.Z,{checked:le,onClick:function(n){n.stopPropagation(),ee((function(n){return z(z({},n),{},(0,i.Z)({},P,le?null:e))}))}},"selected-pipeline-run-".concat(P)))}return!I&&Q&&$.push((0,B.jsx)(f.Z,{flex:1,justifyContent:"flex-end",children:(0,B.jsx)(y._Q,{default:!0,size:C.bL})})),$})),uuid:ye})})}},48381:function(e,n,t){var i=t(82684),r=t(31882),u=t(55485),l=t(30160),o=t(86735),c=t(28598);n.Z=function(e){var n=e.onClickTag,t=e.tags,a=void 0===t?[]:t,s=(0,i.useMemo)((function(){return(null===a||void 0===a?void 0:a.length)||0}),[a]),d=(0,i.useMemo)((function(){return(0,o.YC)(a||[],"uuid")}),[a]);return(0,c.jsx)(u.ZP,{alignItems:"center",flexWrap:"wrap",children:null===d||void 0===d?void 0:d.reduce((function(e,t){return e.push((0,c.jsx)("div",{style:{marginBottom:2,marginRight:s>=2?4:0,marginTop:2},children:(0,c.jsx)(r.Z,{onClick:n?function(){return n(t)}:null,small:!0,children:(0,c.jsx)(l.ZP,{children:t.uuid})})},"tag-".concat(t.uuid))),e}),[])})}},16488:function(e,n,t){t.d(n,{IJ:function(){return m},M8:function(){return Z},Uc:function(){return b},XM:function(){return I},_U:function(){return h},eI:function(){return _},gU:function(){return E},lO:function(){return k},ri:function(){return g},tL:function(){return j},vJ:function(){return P},xH:function(){return x}});var i,r=t(82394),u=t(92083),l=t.n(u),o=t(3917),c=t(4383),a=t(30229),s=t(42122),d=t(86735);function p(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);n&&(i=i.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,i)}return t}function f(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?p(Object(t),!0).forEach((function(n){(0,r.Z)(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):p(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}var h=function(e){return!!e&&!Object.values(a.U5).includes(e)};function m(e){return null===e||void 0===e?void 0:e.reduce((function(e,n){var t=n.block_uuid,i=n.completed_at,u=n.started_at,o=n.status,c=null;u&&i&&(c=l()(i).valueOf()-l()(u).valueOf());return f(f({},e),{},(0,r.Z)({},t,{runtime:c,status:o}))}),{})}var v,g=function(e){var n=[{description:function(){return"This pipeline will run continuously on an interval or just once."},label:function(){return"Schedule"},uuid:a.Xm.TIME},{description:function(){return"This pipeline will run when a specific event occurs."},label:function(){return"Event"},uuid:a.Xm.EVENT},{description:function(){return"Run this pipeline when you make an API call."},label:function(){return"API"},uuid:a.Xm.API}];return e?n.slice(0,1):n};function x(e){var n=(0,s.gR)(e,[a.gm.INTERVAL,a.gm.TYPE]),t=e[a.gm.INTERVAL];t&&(n["schedule_interval[]"]=encodeURIComponent(t));var i=e[a.gm.TYPE];return i&&(n["schedule_type[]"]=i),n}function _(e){return e?new Date(l()(e).valueOf()):null}function b(e,n){return n?(0,o.XG)(e,n):function(e){if("string"!==typeof e)return e;var n=e.split("+")[0];return l()(_(n)).format(o.Nx)}(e)}!function(e){e.DAY="day",e.HOUR="hour",e.MINUTE="minute",e.SECOND="second"}(v||(v={}));var j=(i={},(0,r.Z)(i,v.DAY,86400),(0,r.Z)(i,v.HOUR,3600),(0,r.Z)(i,v.MINUTE,60),(0,r.Z)(i,v.SECOND,1),i);function E(e){var n=v.SECOND,t=e;return e%86400===0?(t/=86400,n=v.DAY):e%3600===0?(t/=3600,n=v.HOUR):e%60===0&&(t/=60,n=v.MINUTE),{time:t,unit:n}}function P(e,n){return e*j[n]}function I(e,n,t){var i,r=l()(e);return r.set("hour",+(null===n||void 0===n?void 0:n.hour)||0),r.set("minute",+(null===n||void 0===n?void 0:n.minute)||0),r.set("second",0),i=r.format(o.TD),null!==t&&void 0!==t&&t.includeSeconds&&(i=i.concat(":00")),null!==t&&void 0!==t&&t.localTimezone&&(i=r.format(o.lE),null!==t&&void 0!==t&&t.convertToUtc&&(i=(0,o.d$)(i,{includeSeconds:null===t||void 0===t?void 0:t.includeSeconds,utcFormat:!0}))),i}function Z(e){var n,t=arguments.length>1&&void 0!==arguments[1]&&arguments[1],i="",r=!0;return r&&(t?i="".concat(window.origin,"/api/pipeline_schedules/").concat(null===e||void 0===e?void 0:e.id,"/api_trigger"):(i="".concat(window.origin,"/api/pipeline_schedules/").concat(null===e||void 0===e?void 0:e.id,"/pipeline_runs"),null!==e&&void 0!==e&&e.token&&(i="".concat(i,"/").concat(e.token)))),r&&(n=window.location.port)&&(i=i.replace(n,c.QT)),i}function y(e,n,t){return e.match(/[*,-/]/)?{additionalOffset:0,cronValue:e}:function(e,n,t){var i=t.indexOf(e),r=0;if(n<0)for(var u=0;u>n;u--)0===i?(i=t.length-1,r-=1):i-=1;else if(n>0)for(var l=0;l<n;l++)i===t.length-1?(i=0,r+=1):i+=1;return{additionalOffset:r,cronValue:String(t[i]||e)}}(+e,n,t)}var O=(0,d.m5)(60),C=(0,d.m5)(24),w=(0,o.Cs)();function k(e,n){if(!e)return e;var t=l()().local().format("Z"),i=t.split(":"),r="-"===t[0],u=3===i[0].length?Number(i[0].slice(1)):Number(i[0]),o=Number(i[1]);(r&&!n||!r&&n)&&(u=-u,o=-o);var c=e.split(" "),a=c[0],s=c[1],d=c[2],p=y(a,o,O),f=y(s,u+p.additionalOffset,C);if(c[0]=p.cronValue,c[1]=f.cronValue,0!==(null===f||void 0===f?void 0:f.additionalOffset)){var h=y(d,f.additionalOffset,w);c[2]=h.cronValue}return c.join(" ")}},44265:function(e,n,t){t.d(n,{Az:function(){return a},BF:function(){return c},Do:function(){return d},IK:function(){return o},P0:function(){return r},VO:function(){return l},sZ:function(){return s}});var i,r,u=t(82394),l=t(41143).V,o=[l.FAILED,l.COMPLETED,l.RUNNING,l.CANCELLED,l.INITIAL],c=[l.INITIAL,l.RUNNING],a=[l.CANCELLED,l.COMPLETED,l.FAILED],s="__mage_variables",d=(i={},(0,u.Z)(i,l.CANCELLED,"Cancelled"),(0,u.Z)(i,l.COMPLETED,"Done"),(0,u.Z)(i,l.FAILED,"Failed"),(0,u.Z)(i,l.INITIAL,"Ready"),(0,u.Z)(i,l.RUNNING,"Running"),i);!function(e){e.PIPELINE_UUID="pipeline_uuid[]",e.STATUS="status[]",e.TAG="pipeline_tag[]"}(r||(r={}))},30229:function(e,n,t){t.d(n,{PN:function(){return o},TR:function(){return h},U5:function(){return a},Wb:function(){return f},Xm:function(){return u},Z4:function(){return s},fq:function(){return c},gm:function(){return d},kJ:function(){return p}});var i,r,u,l=t(82394),o="__bookmark_values__";!function(e){e.API="api",e.EVENT="event",e.TIME="time"}(u||(u={}));var c,a,s=(i={},(0,l.Z)(i,u.API,(function(){return"API"})),(0,l.Z)(i,u.EVENT,(function(){return"event"})),(0,l.Z)(i,u.TIME,(function(){return"schedule"})),i);!function(e){e.ACTIVE="active",e.INACTIVE="inactive"}(c||(c={})),function(e){e.ONCE="@once",e.HOURLY="@hourly",e.DAILY="@daily",e.WEEKLY="@weekly",e.MONTHLY="@monthly",e.ALWAYS_ON="@always_on"}(a||(a={}));var d,p,f=[a.ONCE,a.HOURLY,a.DAILY,a.WEEKLY,a.MONTHLY];!function(e){e.INTERVAL="frequency[]",e.STATUS="status[]",e.TAG="tag[]",e.TYPE="type[]"}(d||(d={})),function(e){e.CREATED_AT="created_at",e.NAME="name",e.PIPELINE="pipeline_uuid",e.STATUS="status",e.TYPE="schedule_type"}(p||(p={}));var h=(r={},(0,l.Z)(r,p.CREATED_AT,"Created at"),(0,l.Z)(r,p.NAME,"Name"),(0,l.Z)(r,p.PIPELINE,"Pipeline"),(0,l.Z)(r,p.STATUS,"Active"),(0,l.Z)(r,p.TYPE,"Type"),r)},31882:function(e,n,t){var i=t(38626),r=t(71180),u=t(55485),l=t(30160),o=t(44897),c=t(72473),a=t(70515),s=t(61896),d=t(28598),p=i.default.div.withConfig({displayName:"Chip__ChipStyle",componentId:"sc-1ok73g-0"})(["display:inline-block;"," "," "," "," "," ",""],(function(e){return!e.primary&&"\n    background-color: ".concat((e.theme.background||o.Z.background).tag,";\n  ")}),(function(e){return e.primary&&"\n    background-color: ".concat((e.theme.chart||o.Z.chart).primary,";\n  ")}),(function(e){return!e.small&&"\n    border-radius: ".concat((a.iI+s.Al)/2,"px;\n    height: ").concat(1.5*a.iI+s.Al,"px;\n    padding: ").concat(a.iI/1.5,"px ").concat(1.25*a.iI,"px;\n  ")}),(function(e){return e.small&&"\n    border-radius: ".concat((a.iI/2+s.Al)/2,"px;\n    height: ").concat(s.Al+a.iI/2+2,"px;\n    padding: ").concat(a.iI/4,"px ").concat(a.iI,"px;\n  ")}),(function(e){return e.xsmall&&"\n    border-radius: ".concat((a.iI/1+s.Al)/1,"px;\n    height: ").concat(20,"px;\n    padding: 4px 6px;\n  ")}),(function(e){return e.border&&"\n    border: 1px solid ".concat((e.theme.content||o.Z.content).muted,";\n  ")}));n.Z=function(e){var n=e.border,t=e.children,i=e.disabled,o=e.label,s=e.monospace,f=e.onClick,h=e.primary,m=e.small,v=e.xsmall;return(0,d.jsx)(p,{border:n,primary:h,small:m,xsmall:v,children:(0,d.jsx)(r.ZP,{basic:!0,disabled:i,noBackground:!0,noPadding:!0,onClick:f,transparent:!0,children:(0,d.jsxs)(u.ZP,{alignItems:"center",children:[t,o&&(0,d.jsx)(l.ZP,{monospace:s,small:m,xsmall:v,children:o}),!i&&f&&(0,d.jsx)("div",{style:{marginLeft:2}}),!i&&f&&(0,d.jsx)(c.x8,{default:h,muted:!h,size:m?a.iI:1.25*a.iI})]})})})}}}]);