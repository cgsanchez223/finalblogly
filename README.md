- The final and complete update to Blogly. First 2 versions can be found here:
    - https://github.com/cgsanchez223/blogly
    - https://github.com/cgsanchez223/blogly2
    - Be sure to review how to install project by following both.

_______________________________________________
- Part 3 adds Mant 2 Many Relationships.
    - Done by adding "tags". Tags are used in social media websites such as Twitter in order to label an article. Clicking on a tag on a post will direct you to a master page with all posts containing that tag.
    - Added is the ability to create tags and add them to a post

- Added Routes:
    - GET /tags - Lists all tags, with links to the tag detail page.
    - GET /tags/[tag-id] - Shows details about specific tag. Also can edit and delete them.
    - GET /tags/new - Form to add new tags
    - POST /tags/new - Process form, adds the tag, and redirects to the tag list page
    - GET /tags/[tag-id]/edit - Edits specified tag
    - POST /tags/[tag-id]/edit - Processes edit form, edits the tag, redirects to tag list
    - POST /tags/[tag-id]/delete - Deletes a tag