(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[36130],{52165:function(e,t,i){Promise.resolve().then(i.bind(i,49352)),Promise.resolve().then(i.bind(i,60881)),Promise.resolve().then(i.bind(i,85337)),Promise.resolve().then(i.bind(i,13162)),Promise.resolve().then(i.bind(i,22376)),Promise.resolve().then(i.bind(i,49421)),Promise.resolve().then(i.bind(i,6067))},69583:function(e,t,i){var o=i(92244),n=i(35147);e.exports=function(e,t){return e&&o(e,t,n)}},20993:function(e,t,i){var o=i(16610),n=i(69583),a=i(60876);e.exports=function(e,t){var i={};return t=a(t,3),n(e,function(e,n,a){o(i,n,t(e,n,a))}),i}},14892:function(e,t,i){"use strict";var o=i(20993),n=i.n(o),a=i(21125);let s=e=>n()(e,e=>"string"==typeof e?(0,a.Z)(e).trim():e);t.Z=(e,t,i,o={})=>({id:e.toLowerCase().replace(/\s/g,"-"),props:s(t),banner:o.banner,codeBanner:o.codeBanner,wrapper:o.wrapper,nonConsoleExample:o.nonConsoleExample,title:e,definition:i})},6067:function(e,t,i){"use strict";var o=i(14892),n=i(59639);let a=function(e,t){let i={props:{onItemClick:{value:"({ detail }) => ['like', 'dislike'].includes(detail.id) && setFeedback(detail.pressed ? detail.id : '')",type:n.Z.Function},feedback:{value:"",type:n.Z.String,stateful:!0,internal:!0}}};return(0,o.Z)(e,{...t},i)},s=`<SpaceBetween size="s">
  <ButtonGroup />
  <Table 
    columnDefinitions={[
      { id: 'name', header: 'File name', cell: (file) => file.name },
      { id: 'size', header: 'File size', cell: (file) => (file.size / 1000) + 'KB' },
    ]}
    items={files}
    empty="No files"
  />
</SpaceBetween>`,r=[a("Default",{variant:"icon",ariaLabel:"Chat actions",items:`[
      {
        type: 'icon-button',
        id: 'copy',
        iconName: 'copy',
        text: 'Copy',
        popoverFeedback: <StatusIndicator type="success">Message copied</StatusIndicator>,
      },
      {
        type: 'icon-button',
        id: 'add',
        iconName: 'add-plus',
        text: 'Add',
      },
      {
        type: 'icon-button',
        id: 'remove',
        iconName: 'remove',
        text: 'Remove',
      },
    ]`}),a("With dropdown menu",{variant:"icon",ariaLabel:"Chat actions",items:`[
      {
        type: 'group',
        text: 'Vote',
        items: [
          {
            type: 'icon-toggle-button',
            id: 'like',
            iconName: 'thumbs-up',
            pressedIconName: 'thumbs-up-filled',
            text: 'Like',
            pressed: feedback === 'like',
          },
          {
            type: 'icon-toggle-button',
            id: 'dislike',
            iconName: 'thumbs-down',
            pressedIconName: 'thumbs-down-filled',
            text: 'Dislike',
            pressed: feedback === 'dislike',
          },
        ],
      },
      {
        type: 'icon-button',
        id: 'copy',
        iconName: 'copy',
        text: 'Copy',
        popoverFeedback: <StatusIndicator type="success">Message copied</StatusIndicator>,
      },
      {
        type: 'menu-dropdown',
        id: 'more-actions',
        text: 'More actions',
        items: [
          {
            id: 'add',
            iconName: 'add-plus',
            text: 'Add',
          },
          {
            id: 'remove',
            iconName: 'remove',
            text: 'Remove',
          },
        ],
      },
    ]`}),a("With an action in progress",{variant:"icon",ariaLabel:"Chat actions",items:`[
      {
        type: 'group',
        text: 'Vote',
        items: [
        {
            type: 'icon-toggle-button',
            id: 'like',
            iconName: 'thumbs-up',
            pressedIconName: 'thumbs-up-filled',
            text: 'Like',
            pressed: false,
            loading: true,
            loadingText: 'Loading',
          },
          {
            type: 'icon-toggle-button',
            id: 'dislike',
            iconName: 'thumbs-down',
            pressedIconName: 'thumbs-down-filled',
            text: 'Dislike',
            pressed: true,
            disabled: true,
          },
        ],
      },
      {
        type: 'icon-button',
        id: 'copy',
        iconName: 'copy',
        text: 'Copy',
        popoverFeedback: <StatusIndicator type="success">Message copied</StatusIndicator>,
      },
      {
        type: 'menu-dropdown',
        id: 'more-actions',
        text: 'More actions',
        items: [
          {
            id: 'add',
            iconName: 'add-plus',
            text: 'Add',
          },
          {
            id: 'remove',
            iconName: 'remove',
            text: 'Remove',
          },
        ],
      },
    ]`}),function(e,t){let i={props:{onFilesChange:{value:"({ detail }) => setFiles(prev => [...prev, ...detail.files])",type:n.Z.Function},files:{value:"[]",type:n.Z.Array,stateful:!0,internal:!0}}};return(0,o.Z)(e,{...t},i,{wrapper:s})}("With file upload",{variant:"icon",ariaLabel:"Chat actions",items:`[
      {
        type: 'icon-file-input',
        id: 'file-input',
        text: 'Upload files',
        multiple: true,
      },
      {
        type: 'icon-button',
        id: 'add',
        iconName: 'add-plus',
        text: 'Add',
      },
      {
        type: 'icon-button',
        id: 'remove',
        iconName: 'remove',
        text: 'Remove',
      },
    ]`})];t.default=r},59639:function(e,t){"use strict";t.Z={String:"string",ReactNode:"react node",Boolean:"boolean",Number:"number",Enum:"enum",Array:"array",Object:"object",Function:"function",Ref:"ref",Date:"date",Custom:"custom"}}},function(e){e.O(0,[81241,47439,81543,76075,46334,38517,53501,93241,60380,25205,12334,62256,99897,67036,12147,80543,27215,96286,42542,53309,15850,37804,90595,63561,91917,17773,74318,30628,93475,2315,4202,19164,62152,50590,71052,39145,30097,74736,95664,92086,73580,44645,83462,24159,58886,86310,68313,50865,12701,99236,58986,52269,96623,15935,43927,6377,21799,28666,80573,17015,54884,71093,11093,44570,61119,60103,63253,70718,63343,32108,54299,90425,58982,90975,15109,82277,87376,88616,5114,77343,19404,50294,48557,87639,60697,614,1438,54039,81293,1528,1744],function(){return e(e.s=52165)}),_N_E=e.O()}]);