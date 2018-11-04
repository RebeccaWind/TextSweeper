class Markup:
    def __init__(self, analyser):
        '''
        Initialise index lists for all cleaning cases with the respective content from the TextAnalyser Object
        :param analyser: instance of the TextCleaner class to make it's class variables accessible
        '''
        self.hyphen = analyser.hyphen_idx
        self.newlines = analyser.newlines_idx
        self.footer = analyser.footer_idx
        self.non_sentences = analyser.non_sentences_idx
        self.sentences = analyser.sents_list
        self.xml_output = ""

    def add_markup(self, number, old_entry, new_entry, cause):
        '''
        Adds markup in XML style according to
        http://www.tei-c.org/release/doc/tei-p5-doc/en/html/PH.html#PHSU    11.3.1.5 Substitutions
        :param number: identification number of the current entry
        :param old_entry: entry to be changed/deleted
        :param new_entry: entry to be added instead of the deleted one
        :param cause: cause of the substitution; currently one of the following four:
                        "hyphenation","newline","footer","non_sentence"
        :return: string that contains the marked-up entry
        '''
        markup = "<subst @n=%s @cause=%s><del>%s</del><add>%s</add></subst>" %(number,cause,old_entry,new_entry)
        return markup

    def markup_all(self):
        '''
        Provides the text with XML-style mark-up for all occurrences that possibly need to be cleaned.
        Mark-up will be added according to the the index-lists for each analysis and cleaning step
        as provided by the TextAnalyser.
        '''
        xml_markup = []
        # Initialise id counter for each case for the attribute @n in the XML markup.
        # Counters are incremented with each successful mark-up addition.
        hyphen_xml_id = 1
        newlines_xml_id = 1
        footer_xml_id = 1
        non_sentence_xml_id = 1
        for i, s in enumerate(self.sentences):
            sent = []
            hyphen_line = self.hyphen[i]
            newline_line = self.newlines[i]
            # initialise a skip index for hyphenation occurrences, as they comprise several indices within a sentence
            skip_idx = 0
            hyphen_counter = 0
            newline_counter = 0

            # mark-up for footers and non-sentences is added per sentence
            if i in self.footer:
                sent.extend("<subst @n=%s @cause=%s><del>" % ("f" + str(footer_xml_id), "footer",))
                footer_xml_id += 1
            elif i in self.non_sentences:
                sent.extend("<subst @n=%s @cause=%s><del>" % ("s" + str(non_sentence_xml_id), "non_sentence",))
                non_sentence_xml_id += 1
            elif hyphen_line is [] and newline_line is []:
                sent.extend(s)

            # mark-up for hyphenation and newlines is added per token
            for idx, token in enumerate(s):
                if idx < skip_idx:
                    continue
                else:
                    skip_idx = idx

                # add markup if the current index (skip_idx) is included in the list of starting indices within the hyphen_line list
                if hyphen_line is not [] and skip_idx in [h[0] for h in hyphen_line]:
                    sent.extend(self.add_markup("h" + str(hyphen_xml_id), "".join(
                        s[hyphen_line[hyphen_counter][0]:hyphen_line[hyphen_counter][1] + 1]),
                                                hyphen_line[hyphen_counter][2], "hyphenation"))
                    hyphen_xml_id += 1
                    # Set the skip_idx to the second value in the hyphenation list entry, so all indices in between will be skipped.
                    skip_idx = hyphen_line[hyphen_counter][1] + 1
                    hyphen_counter += 1

                # Only mark-up newlines if the index was not already contained in the hyphenation list
                elif newline_line is not [] and skip_idx in [n[0] for n in newline_line]:
                    sent.extend(self.add_markup("n" + str(newlines_xml_id), s[newline_line[newline_counter][0]],
                                                newline_line[newline_counter][1], "newline"))
                    newline_counter += 1

                # If no mark-up needs to be done, add the original token to the sent list.
                else:
                    sent.extend(token)

            # Add the second part of the sentence-wide markup started above.
            if i in self.footer or i in self.non_sentences:
                sent.extend("</del><add></add></subst>")

            # Join all mark-up of one sentence and add it to the xml_markup list
            xml_markup.append("".join(sent))

        # Join all mark-up to one string and save it in xml_output.
        self.xml_output = "".join(xml_markup)


    # def markup_hyphens(self, i, sent, idx, token):
    #     #how many occasions of hyphen replacements in the current sentence
    #     hyph_no = len(self.hyphen[i])
    #     k = 0
    #     markup_sent = []
    #     #for each occurrence
    #     for j in range(hyph_no):
    #         while k < self.hyphen[i][j][0]:
    #             markup_sent.append(sent[k])
    #             k += 1
    #         markup_sent.append(self.add_markup("h" + str(hyph_id), "".join(sent[self.hyphen[i][j][0]:self.hyphen[i][j][1] + 1]), self.hyphen[i][j][2], "hyphenation"))
    #         k = self.hyphen[i][j][1]
    #         self.hyph_id += 1
    #     while k < len(sent):
    #         markup_sent.append(sent[k])
    #         k += 1
    #     return(markup_sent)
    #
    # def markup_newlines(self,sent):
    #     newlines_id = 1
    #     # how many occasions of newline replacements in the current sentence
    #     newlines_no = len(self.newlines[i])
    #     k = 0
    #     # for each occurrence
    #     for j in range(newlines_no):
    #         while k < self.newlines[i][j][0]:
    #             sent.append(s[k])
    #             k += 1
    #         sent.append(self.add_markup("n" + str(newlines_id),s[self.newlines[i][j][0]],self.newlines[i][j][2],"newline"))
    #         k += 1
    #         newlines_id += 1
    #
    # def markup_footers(self,sent):
    #     footers_id = 1
    #     sent.append(self.add_markup("f"+str(footers_id),"".join(s),"","footer"))
    #     footers_id += 1
    #
    # def markup_non_sentences(self,sent):
    #     non_sentences_id = 1
    #     sent.append(self.add_markup("f" + str(non_sentences_id), "".join(s), "", "non-sentence"))
    #     non_sentences_id += 1

