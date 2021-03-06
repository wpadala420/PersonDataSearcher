import twint

c = twint.Config()
c.Search = "from:drdr_zz"

twint.run.Search(c)