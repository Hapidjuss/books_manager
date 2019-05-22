class BookHelper:
    item_unknown: str = 'unknown'

    def add_item(self, tag=None):
        if tag is not None:
            return tag
        else:
            return self.item_unknown

    def add_items(self, table_object, attribute, database, tag_list=None):
        if tag_list is not None:
            item_list = []
        
            for item in tag_list:                               # is item in database already?...
                new_item = table_object.query.filter(getattr(table_object, attribute) == item).first()
                if new_item is None:
                    new_item = table_object(item)
                    database.session.add(new_item)              # ...add one if not
                item_list.append(new_item)
            return item_list        # [item1, item2,...]
        else:                                                   # --//--
            new_item = table_object.query.filter(getattr(table_object, attribute) == self.item_unknown).first()
            if new_item is None:
                new_item = table_object(self.item_unknown)
                database.session.add(new_item)                  # --//--
            return new_item         # 'unknown'

    def test_dublicate(self, book_object, book):
        books = book_object.query.filter(book_object.title == book.title).all()
        if not books:
            return False
        for b in books:
            if b.description == book.description:
                for i in range(len(b.authors)):
                    if b.authors[i].name != book.authors[i].name:
                        return False
                for j in range(len(b.categories)):
                    if b.categories[j].category_name != book.categories[j].category_name:
                        return False
                return True
            else:
                return False
        return True
