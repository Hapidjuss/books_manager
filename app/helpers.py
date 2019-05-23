class BookHelper:
    item_unknown: str = 'unknown'

    @staticmethod
    def test_duplicate(book_object, book):
        books = book_object.query.filter(book_object.title == book.title).all()
        if not books:               # empty database
            return False
        for b in books:             # books need to have the same _title_ and _authors_ for return value True
            if len(b.authors) == len(book.authors):
                test = False
                for a in book.authors:              # check if authors are in different order but the same
                    test = any(author.name == a.name for author in b.authors)
                    if not test:
                        break
                if test:
                    return True
        return False

    # helper for title and description tag
    def add_item(self, tag=None):
        if tag is not None:
            return tag
        else:
            return self.item_unknown

    # helper for authors and categories tag
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
