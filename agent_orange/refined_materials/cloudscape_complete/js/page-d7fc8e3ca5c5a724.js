(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[92094],{19057:function(e,t,n){Promise.resolve().then(n.bind(n,49352)),Promise.resolve().then(n.bind(n,60881)),Promise.resolve().then(n.bind(n,40596)),Promise.resolve().then(n.bind(n,85337)),Promise.resolve().then(n.bind(n,13162)),Promise.resolve().then(n.bind(n,22376)),Promise.resolve().then(n.bind(n,49421)),Promise.resolve().then(n.bind(n,34636))},69583:function(e,t,n){var o=n(92244),i=n(35147);e.exports=function(e,t){return e&&o(e,t,i)}},20993:function(e,t,n){var o=n(16610),i=n(69583),r=n(60876);e.exports=function(e,t){var n={};return t=r(t,3),i(e,function(e,i,r){o(n,i,t(e,i,r))}),n}},14892:function(e,t,n){"use strict";var o=n(20993),i=n.n(o),r=n(21125);let a=e=>i()(e,e=>"string"==typeof e?(0,r.Z)(e).trim():e);t.Z=(e,t,n,o={})=>({id:e.toLowerCase().replace(/\s/g,"-"),props:a(t),banner:o.banner,codeBanner:o.codeBanner,wrapper:o.wrapper,nonConsoleExample:o.nonConsoleExample,title:e,definition:n})},40596:function(e,t,n){"use strict";n.d(t,{ComponentTestingGuidelines:function(){return a}});var o=n(27573);n(7653);var i=n(23887),r=n(30208);function a(){let e=(0,r.ND)();return(0,o.jsxs)(o.Fragment,{children:[(0,o.jsx)("p",{children:"These components are distributed in a separate package. To find them in test-utils, add an extra import along with the main test-utils import:"}),(0,o.jsx)("h3",{children:"For unit testing"}),(0,o.jsx)(i.Z,{code:`
// side-effect import to install the finder methods
import '${e.packageNames.boards}/test-utils/dom';
// use import from the main package to use the wrapper
import createWrapper from '${e.packageNames.components}/test-utils/dom';

createWrapper().findBoard().getElement();
        `}),(0,o.jsx)("h3",{children:"For integration testing"}),(0,o.jsx)(i.Z,{code:`
// side-effect import to install the finder methods
import '${e.packageNames.boards}/test-utils/selectors';
// use import from the main package to use the wrapper
import createWrapper from '${e.packageNames.components}/test-utils/selectors';

createWrapper().findBoard().toSelector();
        `})]})}},30208:function(e,t,n){"use strict";n.d(t,{ND:function(){return s}});var o=n(27573),i=n(7653),r=n(87350);let a=(0,i.createContext)(null);function s(){let e=(0,i.useContext)(a);if(!e)throw Error("useSiteConfig must be used within a SiteConfigProvider");return e}t.ZP=({children:e})=>(0,o.jsx)(a.Provider,{value:(0,r.Z)(),children:e})},34636:function(e,t,n){"use strict";var o=n(14892),i=n(25505),r=n(59639);let a=`(item) => <BoardItem
  header={<Header>{item.data.title}</Header>}
  i18nStrings={${i.Rh}}
>
  {item.data.content}
</BoardItem>`,s=`(item, actions) => <BoardItem
  header={<Header>{item.data.title}</Header>}
  i18nStrings={${i.Rh}}
  settings={
    <ButtonDropdown
      items={[
        { id: 'remove', text: 'Remove' }
      ]}
      ariaLabel="Board item settings"
      variant="icon"
      onItemClick={() => actions.removeItem()}
    />
  }
>
  {item.data.content}
</BoardItem>`,c=function(e,t){return(0,o.Z)(e,{i18nStrings:i.CX,renderItem:a,...t},{props:{renderItem:{type:r.Z.Object},onItemsChange:{value:"(event) => setItems(event.detail.items)",type:r.Z.Function},items:{type:r.Z.Object,stateful:!0}}})},m=[{id:"1",rowSpan:1,columnSpan:2,data:{title:"Demo 1",content:"First item"}},{id:"2",rowSpan:1,columnSpan:2,data:{title:"Demo 2",content:"Second item"}},{id:"3",rowSpan:1,columnSpan:3,data:{title:"Demo 3",content:"Third item"}}],d=`<Box margin={{ vertical: 'xs' }} textAlign="center" color="inherit">
  <SpaceBetween size="m">
    <Box variant="strong" color="inherit">No items</Box>
    <Button iconName="add-plus">Add an item</Button>
  </SpaceBetween>
</Box>`,l=[c("Simple",{items:m}),c("Removable items",{items:m,renderItem:s,empty:d}),c("Empty",{items:[],empty:d})];t.default=l},25505:function(e,t,n){"use strict";n.d(t,{CX:function(){return o},Rh:function(){return i},kh:function(){return r}});let o=`(() => {
  function createAnnouncement(operationAnnouncement, conflicts, disturbed) {
    const conflictsAnnouncement =
      conflicts.length > 0 ? \`Conflicts with $\{conflicts.map(c => c.data.title).join(', ')}.\` : '';
    const disturbedAnnouncement = disturbed.length > 0 ? \`Disturbed $\{disturbed.length} items.\` : '';
    return [operationAnnouncement, conflictsAnnouncement, disturbedAnnouncement].filter(Boolean).join(' ');
  }
  return {
    liveAnnouncementDndStarted: operationType => (operationType === 'resize' ? 'Resizing' : 'Dragging'),
    liveAnnouncementDndItemReordered: operation => {
      const columns = \`column $\{operation.placement.x + 1}\`;
      const rows = \`row $\{operation.placement.y + 1}\`;
      return createAnnouncement(
        \`Item moved to $\{operation.direction === 'horizontal' ? columns : rows}.\`,
        operation.conflicts,
        operation.disturbed
      );
    },
    liveAnnouncementDndItemResized: operation => {
      const columnsConstraint = operation.isMinimalColumnsReached ? ' (minimal)' : '';
      const rowsConstraint = operation.isMinimalRowsReached ? ' (minimal)' : '';
      const sizeAnnouncement =
        operation.direction === 'horizontal'
          ? \`columns $\{operation.placement.width}$\{columnsConstraint}\`
          : \`rows $\{operation.placement.height}$\{rowsConstraint}\`;
      return createAnnouncement(\`Item resized to $\{sizeAnnouncement}.\`, operation.conflicts, operation.disturbed);
    },
    liveAnnouncementDndItemInserted: operation => {
      const columns = \`column $\{operation.placement.x + 1}\`;
      const rows = \`row $\{operation.placement.y + 1}\`;
      return createAnnouncement(\`Item inserted to $\{columns}, $\{rows}.\`, operation.conflicts, operation.disturbed);
    },
    liveAnnouncementDndCommitted: operationType => \`$\{operationType} committed\`,
    liveAnnouncementDndDiscarded: operationType => \`$\{operationType} discarded\`,
    liveAnnouncementItemRemoved: op => createAnnouncement(\`Removed item $\{op.item.data.title}.\`, [], op.disturbed),
    navigationAriaLabel: 'Board navigation',
    navigationAriaDescription: 'Click on non-empty item to move focus over',
    navigationItemAriaLabel: item => (item ? item.data.title : 'Empty'),
  };
})()`,i=`{
  dragHandleAriaLabel: 'Drag handle',
  dragHandleAriaDescription:
    'Use Space or Enter to activate drag, arrow keys to move, Space or Enter to submit, or Escape to discard. Be sure to temporarily disable any screen reader navigation feature that may interfere with the functionality of the arrow keys.',
  resizeHandleAriaLabel: 'Resize handle',
  resizeHandleAriaDescription:
    'Use Space or Enter to activate resize, arrow keys to move, Space or Enter to submit, or Escape to discard. Be sure to temporarily disable any screen reader navigation feature that may interfere with the functionality of the arrow keys.',
}`,r=`{
  navigationAriaLabel: 'Items palette navigation',
  navigationAriaDescription: 'Click on an item to move focus over',
  navigationItemAriaLabel: item => item.data.title,
  liveAnnouncementDndStarted: 'Dragging',
  liveAnnouncementDndDiscarded: 'Insertion discarded',
}`},59639:function(e,t){"use strict";t.Z={String:"string",ReactNode:"react node",Boolean:"boolean",Number:"number",Enum:"enum",Array:"array",Object:"object",Function:"function",Ref:"ref",Date:"date",Custom:"custom"}}},function(e){e.O(0,[81241,47439,81543,76075,46334,38517,53501,93241,60380,25205,12334,62256,99897,67036,42542,12147,80543,27215,96286,53309,15850,37804,90595,63561,91917,17773,74318,30628,93475,2315,4202,19164,62152,50590,71052,39145,30097,74736,95664,92086,73580,44645,83462,24159,58886,86310,68313,50865,12701,99236,58986,52269,96623,15935,43927,6377,21799,28666,80573,17015,54884,71093,11093,44570,61119,60103,63253,70718,63343,32108,54299,90425,58982,90975,15109,82277,87376,88616,5114,77343,19404,50294,48557,87639,60697,614,1438,54039,81293,1528,1744],function(){return e(e.s=19057)}),_N_E=e.O()}]);