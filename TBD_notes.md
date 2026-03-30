## Cases

1) html (whole document) : use soup.html

2) body : use soup.body

3) sub-tree (fragment): use soup.children



## 'Tag' case:
(The use case for this was in sandstone where we had body markup div's inside of post typography div's.)

Then we are passed only a subtree and we cannot call soup.html or soup.body, but we can call soup.children

The problem is, what is the test for this 'Tag' case? There isn't one.

## Questions
- Why can't we just always use soup.children?

## Notes
- I don't give a shit about removing Doctype entries.

