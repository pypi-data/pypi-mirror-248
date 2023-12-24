    @property
    def ^{obj}^_list(self):
        return [x for x in ^{Obj}^.query({'^{ref}^_id': self.key})]

