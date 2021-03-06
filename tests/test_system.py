# -*- coding: utf-8 -*-
"""
test_system
========

Test image processing on images from examples

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging

log = logging.getLogger(__name__)

import chemschematicresolver as csr
import os
import unittest
import copy

from skimage import img_as_float
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches


tests_dir = os.path.dirname(os.path.abspath(__file__))
train_dir = os.path.join(os.path.dirname(tests_dir), 'train')
examples_dir = os.path.join(train_dir, 'train_imgs')
markush_dir = os.path.join(train_dir, 'train_markush_small')
r_group_diags_dir = os.path.join(train_dir, 'r_group_diags')
labelled_output_dir = os.path.join(train_dir, 'output')

class TestSystem(unittest.TestCase):

    # Testing that the images are being cleaned of floating pixels
    def do_diag_clean(self, filename, filedir=examples_dir):
        """
        Tests that rouge pixel islands are removed for all diagrams in filename.
        Displays the individual diagram areas for human inspection
        :param filename
        :return:
        """

        test_diag = os.path.join(filedir, filename)

        fig = csr.io.imread(test_diag) # Read in float and raw pixel images
        raw_fig = copy.deepcopy(fig)  # Create unreferenced binary copy

        panels = csr.actions.segment(raw_fig)
        print('Segmented panel number : %s ' % len(panels))

        labels, diags = csr.actions.classify_kmeans(panels)
        labels, diags = csr.actions.preprocessing(labels, diags, fig)
        all_panels = labels + diags
        print('After processing : %s' % len(all_panels))

        # Show diagrams in blue
        for panel in diags:

            # Create output image
            out_fig, ax = plt.subplots(figsize=(10, 6))
            ax.imshow(panel.fig.img)

            ax.set_axis_off()
            plt.show()

    def test_diag_clean_all(self):
        """
        Test all diagrams in train_imgs
        :return:
        """

        test_path = examples_dir
        test_imgs = os.listdir(test_path)
        for img_path in test_imgs:
            self.do_diag_clean(img_path, filedir=test_path)

    def test_diag_clean_1(self):
        self.do_diag_clean('S0143720816301681_gr1.jpg')

    def test_diag_clean_2(self):
        self.do_diag_clean('S014372081630122X_gr1.jpg')

    def test_diag_clean_3(self):
        self.do_diag_clean('S0143720816301565_gr1.jpg', filedir=r_group_diags_dir)


    # Testing sementation is sucessful
    def do_segmentation(self, filename, filedir=examples_dir):
        '''
        Tests bounding box assignment for filename, and kmeans classification into diagrams (blue) and labels (red)

        :param filename:
        :return:
        '''

        test_diag = os.path.join(filedir, filename)

        fig = csr.io.imread(test_diag) # Read in float and raw pixel images
        raw_fig = copy.deepcopy(fig)  # Create unreferenced binary copy

        panels = csr.actions.segment(raw_fig, size=3)
        print('Segmented panel number : %s ' % len(panels))

        labels, diags = csr.actions.classify_kmeans(panels)
        labels, diags = csr.actions.preprocessing(labels, diags, fig)
        all_panels = labels + diags
        print('After processing : %s' % len(all_panels))

        # Create output image
        out_fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(fig.img)

        # Show diagrams in blue
        for panel in diags:

            diag_rect = mpatches.Rectangle((panel.left, panel.top), panel.width, panel.height,
                                           fill=False, edgecolor='b', linewidth=2)
            ax.text(panel.left, panel.top + panel.height / 4, '[%s]' % panel.tag, size=panel.height / 20, color='r')
            ax.add_patch(diag_rect)

        # Show labels in red
        for panel in labels:

            diag_rect = mpatches.Rectangle((panel.left, panel.top), panel.width, panel.height,
                                           fill=False, edgecolor='r', linewidth=2)
            ax.text(panel.left, panel.top + panel.height / 4, '[%s]' % panel.tag, size=panel.height / 20, color='r')
            ax.add_patch(diag_rect)

        ax.set_axis_off()
        plt.show()


    def test_segmentation_all(self):

        test_path = examples_dir
        test_imgs = os.listdir(test_path)
        for img_path in test_imgs:
            self.do_segmentation(img_path, filedir=test_path)

    def test_variable_cases(self):

        self.do_segmentation('S0143720816300286_gr1.jpg')
        self.do_segmentation('S0143720816301115_gr1.jpg')
        self.do_segmentation('S0143720816301115_gr4.jpg')
        self.do_segmentation('S014372081630167X_sc1.jpg')

    def test_segmentation1(self):

        self.do_segmentation('S014372081630119X_gr1.jpg')

    def test_segmentation2(self):
        self.do_segmentation('S014372081630122X_gr1.jpg')

    def test_segmentation3(self):
        # TODO : noise remover? Get rid of connected components a few pixels in size?
        self.do_segmentation('S014372081630167X_sc1.jpg') # This one isn't identifying the repeating unit, or label

    def test_segmentation4(self):
        self.do_segmentation('S014372081730116X_gr8.jpg')

    def test_segmentation5(self):
        self.do_segmentation('S0143720816300201_sc2.jpg')

    def test_segmentation6(self):
        self.do_segmentation('S0143720816300274_gr1.jpg')

    def test_segmentation7(self):
        self.do_segmentation('S0143720816300419_sc1.jpg')

    def test_segmentation8(self):
        self.do_segmentation('S0143720816300559_sc2.jpg')

    def test_segmentation9(self):
        self.do_segmentation('S0143720816300821_gr2.jpg')

    def test_segmentation10(self):
        self.do_segmentation('S0143720816300900_gr2.jpg')

    def test_segmentation11(self):
        self.do_segmentation('S0143720816301115_gr1.jpg')

    def test_segmentation12(self):
        self.do_segmentation('S0143720816301115_gr4.jpg')

    def test_segmentation_markush_img(self):
        self.do_segmentation('S0143720816301115_r75.jpg')

    def test_segmentation_markush_img2(self):
        self.do_segmentation('S0143720816300286_gr1.jpg')

    def test_segmentation_markush_img3(self):
        self.do_segmentation('S0143720816301681_gr1.jpg')

    def test_segmentation_r_group_diags_img1(self):
        self.do_segmentation('S0143720816301565_gr1.jpg', r_group_diags_dir)

    def test_segmentation_r_group_diags_img2(self):
        self.do_segmentation('S0143720816302054_sc1.jpg', filedir=r_group_diags_dir)

    def test_segmentation_r_group_diags_img3(self):

        self.do_segmentation('S0143720816301401_gr5.jpg', r_group_diags_dir)

    def test_segmentation_13(self):
        self.do_segmentation('10.1039_C4TC01753F_fig1.gif', filedir='/home/edward/github/csr-development/csd')

    # Testing grouping of diagram - label pairs is correct
    def do_grouping(self, filename, filedir=examples_dir):
        '''
        Tests grouping of label-diagram pairs, where label and diagram have the same coloured bbox
        To be checked by a human

        :param filename:
        :return:
        '''

        test_diag = os.path.join(filedir, filename)

        # Read in float and raw pixel images
        fig = csr.io.imread(test_diag)
        fig_bbox = fig.get_bounding_box()

        # Create unreferenced binary copy
        bin_fig = copy.deepcopy(fig)

        # Segment and classify diagrams
        panels = csr.actions.segment(bin_fig)
        labels, diags = csr.actions.classify_kmeans(panels)

        # Preprocessing cleaning and merging
        labels, diags = csr.actions.preprocessing(labels, diags, fig)

        # Create output image
        out_fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(fig.img)

        # Assign labels to diagrams
        labelled_diags = csr.actions.label_diags(labels, diags, fig_bbox)

        colours = iter(['r', 'b', 'g', 'k', 'c', 'm', 'y', 'r', 'b', 'g', 'k', 'c', 'm', 'y', 'r', 'b', 'g', 'k', 'c', 'm', 'y'])

        for diag in labelled_diags:
            colour = next(colours)

            diag_rect = mpatches.Rectangle((diag.left, diag.top), diag.width, diag.height,
                                      fill=False, edgecolor=colour, linewidth=2)
            ax.add_patch(diag_rect)

            label = diag.label
            label_rect = mpatches.Rectangle((label.left, label.top), label.width, label.height,
                                      fill=False, edgecolor=colour, linewidth=2)
            ax.add_patch(label_rect)

        ax.set_axis_off()
        plt.show()

    def test_grouping_all(self):
        test_path = examples_dir
        test_imgs = os.listdir(test_path)
        for img_path in test_imgs:
            print(img_path)
            self.do_grouping(img_path, filedir=test_path)

    def test_grouping1(self):
        self.do_grouping('S014372081630119X_gr1.jpg')

    def test_grouping2(self):
        self.do_grouping('S014372081630122X_gr1.jpg')

    def test_grouping3(self):
        self.do_grouping('S014372081630167X_sc1.jpg')

    def test_grouping4(self):
        self.do_grouping('S014372081730116X_gr8.jpg')

    def test_grouping5(self):
        self.do_grouping('S0143720816300201_sc2.jpg')

    def test_grouping6(self):
        self.do_grouping('S0143720816300274_gr1.jpg')

    def test_grouping7(self):
        self.do_grouping('S0143720816300419_sc1.jpg')

    def test_grouping8(self):
        self.do_grouping('S0143720816300559_sc2.jpg')

    def test_grouping9(self):
        self.do_grouping('S0143720816300821_gr2.jpg')

    def test_grouping10(self):
        self.do_grouping('S0143720816300900_gr2.jpg')

    def test_grouping_r_group_diags(self):
        self.do_grouping('S0143720816302054_sc1.jpg', filedir=r_group_diags_dir)

    def test_grouping_markush(self):
        self.do_grouping('S0143720816300286_gr1.jpg')

    def do_ocr(self, filename, filedir=examples_dir):
        """ Tests the OCR recognition of labels."""

        test_diag = os.path.join(filedir, filename)

        # Read in float and raw pixel images
        fig = csr.io.imread(test_diag)
        fig_bbox = fig.get_bounding_box()

        # Create unreferenced binary copy
        bin_fig = copy.deepcopy(fig)

        # Segment and classify diagrams and labels
        panels = csr.actions.segment(bin_fig)
        labels, diags = csr.actions.classify_kmeans(panels)
        labels, diags = csr.actions.preprocessing(labels, diags, fig)

        # Create output image
        out_fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(fig.img)

        # Assign labels to diagrams
        labelled_diags = csr.actions.label_diags(labels, diags, fig_bbox)

        colours = iter(
            ['r', 'b', 'g', 'k', 'c', 'm', 'y', 'r', 'b', 'g', 'k', 'c', 'm', 'y', 'r', 'b', 'g', 'k', 'c', 'm', 'y'])

        labels_text = []

        for diag in labelled_diags:
            colour = next(colours)

            diag_rect = mpatches.Rectangle((diag.left, diag.top), diag.width, diag.height,
                                           fill=False, edgecolor=colour, linewidth=2)
            ax.text(diag.left, diag.top + diag.height / 4, '[%s]' % diag.tag, size=diag.height / 20, color='r')
            ax.add_patch(diag_rect)

            label = diag.label
            label_rect = mpatches.Rectangle((label.left, label.top), label.width, label.height,
                                            fill=False, edgecolor=colour, linewidth=2)
            ax.text(label.left, label.top + label.height / 4, '[%s]' % label.tag, size=label.height / 5, color='r')
            ax.add_patch(label_rect)

            label = csr.actions.read_label(fig, label)
            label_strings = [csr.actions.clean_output(sentence.text) for sentence in label.text]
            labels_text.append(label_strings)
            print("Label %s : %s " % (label.tag, labels_text))

        ax.set_axis_off()
        plt.show()

        return labels_text

    def test_ocr_all(self):

        test_path = examples_dir
        test_imgs = os.listdir(test_path)
        for img_path in test_imgs:
            self.do_ocr(img_path, filedir=test_path)

    def test_ocr1(self):
        labels_text = self.do_ocr('S014372081630119X_gr1.jpg')
        gold = [['MeNAPH:R=CH3', 'MeONAPH:R=OCH3'], ['EtNAPH']]
        self.assertListEqual(gold, labels_text)

    # TODO : Update all OCR tests to reflect new format

    def test_ocr2(self):
        labels_text = self.do_ocr('S014372081630122X_gr1.jpg')
        gold = [['Q4'], ['Q1'], ['Q2'], ['Q3']]
        self.assertEqual(gold, labels_text)

    def test_ocr3(self):
        # Currently failing - not getting B in the second label
        labels_text = self.do_ocr('S014372081630167X_sc1.jpg')
        gold = [['TPE-SQ'], ['PC71BM']]
        self.assertEqual(gold, labels_text)

    def test_ocr4(self):
        labels_text = self.do_ocr('S014372081730116X_gr8.jpg')
        gold = [['J51'], ['PDBT-T1'], ['J61'], ['R=2-ethylhexyl', 'PBDB-T'], ['R=2-ethylhexyl', 'PBDTTT-E-T'], ['R=2-ethylhexyl', 'PTB7-Th'],
                ['R=2-ethylhexyl', 'PBDTTT-C-T']]
        for item in gold:
            self.assertIn(item, labels_text)

    def test_ocr5(self):
        labels_text = self.do_ocr('S0143720816300201_sc2.jpg')
        gold = [['9(>99%)'], ['1(82%)'], ['3(86%)'], ['7(94%)'],
                ['4(78%)'], ['5(64%)'], ['2(78%)'], ['6(75%)'], ['8(74%)']]
        for x in gold:
            self.assertIn(x, labels_text)

    def test_ocr6(self):
        labels = self.do_ocr('S0143720816300274_gr1.jpg')
        gold = [['8c'], ['8b'], ['8a'], ['7c'], ['7b'], ['7a']]
        for x in gold:
            self.assertIn(x, labels)

    def test_ocr7(self):
        labels = self.do_ocr('S0143720816300419_sc1.jpg')
        gold = [['DDOF'], ['DPF'], ['NDOF'], ['PDOF']]
        for x in gold:
            self.assertIn(x, labels)

    def test_ocr8(self):
        labels = self.do_ocr('S0143720816300559_sc2.jpg')
        gold = [['1'], ['2'], ['3']]
        for x in gold:
            self.assertIn(x, labels)

    def test_ocr9(self):
        labels = self.do_ocr('S0143720816300821_gr2.jpg') # Need to add greyscale
        gold = [['9'], ['10']]
        for x in gold:
            self.assertIn(x, labels)

    def test_ocr10(self):
        # IR dye doesn't work
        labels = self.do_ocr('S0143720816300900_gr2.jpg')
        gold = [['ICG'], ['Compound10'], ['Compound13'], ['Compound11'], ['ZW800-1'], ['Compound12']]
        for x in gold:
            self.assertIn(x, labels)

    def test_ocr11(self):
        # Currently failing - can't detect some :
        labels = self.do_ocr('S0143720816301115_gr1.jpg')
        gold = [['1:R1=R2=H:TQEN'], ['2:R1=H,R2=OMe:T(MQ)EN'], ['3:R1=R2=OMe:T(TMQ)EN']]
        for x in gold:
            self.assertIn(x, labels)

    def do_r_group(self, filename, debug=False, filedir=examples_dir):
        """ Tests the R-group detection and recognition """

        test_diag = os.path.join(filedir, filename)

        # Read in float and raw pixel images
        fig = csr.io.imread(test_diag)
        fig_bbox = fig.get_bounding_box()

        # Create unreferenced binary copy
        bin_fig = copy.deepcopy(fig)

        # Segment and classify diagrams and labels
        panels = csr.actions.segment(bin_fig)
        labels, diags = csr.actions.classify_kmeans(panels)
        labels, diags = csr.actions.preprocessing(labels, diags, fig)

        # Create output image
        if debug is True:
            out_fig, ax = plt.subplots(figsize=(10, 6))
            ax.imshow(fig.img)
            colours = iter(
                ['r', 'b', 'g', 'k', 'c', 'm', 'y', 'r', 'b', 'g', 'k', 'c', 'm', 'y', 'r', 'b', 'g', 'k', 'c', 'm',
                 'y'])

        labelled_diags = csr.actions.label_diags(labels, diags, fig_bbox)

        for diag in labelled_diags:

            label = diag.label
            diag.label = csr.actions.read_label(fig, label)
            diag = csr.r_group.detect_r_group(diag)

            if debug is True:

                colour = next(colours)

                diag_rect = mpatches.Rectangle((diag.left, diag.top), diag.width, diag.height,
                                               fill=False, edgecolor=colour, linewidth=2)
                ax.text(diag.left, diag.top + diag.height / 4, '[%s]' % diag.tag, size=diag.height / 20, color='r')
                ax.add_patch(diag_rect)

                label_rect = mpatches.Rectangle((label.left, label.top), label.width, label.height,
                                                fill=False, edgecolor=colour, linewidth=2)
                ax.text(label.left, label.top + label.height / 4, '[%s]' % label.tag, size=label.height / 5, color='r')
                ax.add_patch(label_rect)

                print(diag.label.r_group)

        if debug is True:
            ax.set_axis_off()
            plt.show()

        return labelled_diags

    def test_r_group_detection_all(self):

        test_path = examples_dir
        test_imgs = os.listdir(test_path)
        for img_path in test_imgs:
            self.do_ocr(img_path, filedir=test_path)

    def test_r_group1(self):
        labelled_diags = self.do_r_group('S014372081630119X_gr1.jpg')
        all_detected_r_groups_values = [(token[0].text, token[1].text)for diag in labelled_diags for tokens
                                        in diag.label.r_group for token in tokens]
        gold = [('R', 'OCH3'), ('R', 'CH3')]
        for x in gold:
            self.assertIn(x, all_detected_r_groups_values)

    def test_r_group2(self):
        """ Tests included to check the rgroup variable is unpopulated"""
        labelled_diags = self.do_r_group('S014372081630122X_gr1.jpg')
        all_detected_r_groups_values = [token[1].text for diag in labelled_diags for tokens in diag.label.r_group for token in tokens]
        self.assertTrue(len(all_detected_r_groups_values) is 0)

    def test_r_group3(self):
        labelled_diags = self.do_r_group('S014372081630167X_sc1.jpg')
        all_detected_r_groups_values = [token[1].text for diag in labelled_diags for tokens in diag.label.r_group for token in tokens]
        self.assertTrue(len(all_detected_r_groups_values) is 0)

    def test_r_group4(self):
        labelled_diags = self.do_r_group('S014372081730116X_gr8.jpg')
        all_detected_r_groups_values = [tokens for diag in labelled_diags for tokens in diag.label.r_group]
        unique_combos = []
        for tokens in all_detected_r_groups_values:
            tuple_set = set()
            for token in tokens:
                tuple_set.add((token[0].text, token[1].text))
            unique_combos.append(tuple_set)

        gold = {('R', '2-ethylhexyl')}  # All R-groups give this for this example
        for diag in unique_combos:
            self.assertEqual(diag, gold)

        self.assertEqual(len(unique_combos), 4)

    def test_r_group5(self):
        labelled_diags = self.do_r_group('S0143720816300201_sc2.jpg')
        all_detected_r_groups_values = [token[1].text for diag in labelled_diags for tokens in diag.label.r_group for token in tokens]
        self.assertTrue(len(all_detected_r_groups_values) is 0)

    def test_r_group6(self):
        labelled_diags = self.do_r_group('S0143720816300274_gr1.jpg')
        all_detected_r_groups_values = [token[1].text for diag in labelled_diags for tokens in diag.label.r_group for token in tokens]
        self.assertTrue(len(all_detected_r_groups_values) is 0)

    def test_r_group7(self):
        labelled_diags = self.do_r_group('S0143720816300419_sc1.jpg')
        all_detected_r_groups_values = [token[1].text for diag in labelled_diags for tokens in diag.label.r_group for token in tokens]
        self.assertTrue(len(all_detected_r_groups_values) is 0)

    def test_r_group8(self):
        labelled_diags = self.do_r_group('S0143720816300559_sc2.jpg')
        all_detected_r_groups_values = [token[1].text for diag in labelled_diags for tokens in diag.label.r_group for token in tokens]
        self.assertTrue(len(all_detected_r_groups_values) is 0)

    def test_r_group9(self):
        labelled_diags = self.do_r_group('S0143720816300821_gr2.jpg')
        all_detected_r_groups_values = [token[1].text for diag in labelled_diags for tokens in diag.label.r_group for token in tokens]
        self.assertTrue(len(all_detected_r_groups_values) is 0)

    def test_r_group10(self):
        labelled_diags = self.do_r_group('S0143720816300900_gr2.jpg')
        all_detected_r_groups_values = [token[1].text for diag in labelled_diags for tokens in diag.label.r_group for token in tokens]
        self.assertTrue(len(all_detected_r_groups_values) is 0)

    def test_r_group11(self):
        # Currently failing : OCR performing poorly on semicolons
        labelled_diags = self.do_r_group('S0143720816301115_r75.jpg')
        all_detected_r_groups_values = [(token[0].text, token[1].text) for diag in labelled_diags for tokens in diag.label.r_group for token in tokens]
        gold = [('X', 'S'), ('X', 'O')]
        for x in gold:
            self.assertIn(x, all_detected_r_groups_values)

    def test_r_group12(self):
        labelled_diags = self.do_r_group('S0143720816301681_gr1.jpg')
        all_detected_r_groups_values = [tokens for diag in labelled_diags for tokens in diag.label.r_group]
        unique_combos = []
        for tokens in all_detected_r_groups_values:
            tuple_set = set()
            for token in tokens:
                tuple_set.add((token[0].text, token[1].text))
            unique_combos.append(tuple_set)

        gold = [{('R', 'CN'), ('X', 'NH')}, {('R', 'CN'), ('X', 'NC(O)OEt')}, {('R', 'CN'), ('X', 'O')}, {('R', 'H'), ('X', 'O')}]
        for diag in unique_combos:
            self.assertIn(diag, gold)

    def do_label_smile_resolution(self, filename, debug=True, filedir=examples_dir):
        """ Tests the R-group detection, recognition and resolution (using OSRA)
        NB : This is very similar to extract.extract_diagram, but it does not filter out the wildcard results
        This can be helpful to identify where OSRA is failing
        """

        r_smiles = []
        smiles = []

        test_diag = os.path.join(filedir, filename)

        # Read in float and raw pixel images
        fig = csr.io.imread(test_diag)
        fig_bbox = fig.get_bounding_box()

        # Create unreferenced binary copy
        bin_fig = copy.deepcopy(fig)

        # Segment and classify diagrams and labels
        panels = csr.actions.segment(bin_fig)
        labels, diags = csr.actions.classify_kmeans(panels)
        labels, diags = csr.actions.preprocessing(labels, diags, fig)

        # Create output image
        if debug is True:
            out_fig, ax = plt.subplots(figsize=(10, 6))
            ax.imshow(fig.img)
            colours = iter(
                ['r', 'b', 'g', 'k', 'c', 'm', 'y', 'r', 'b', 'g', 'k', 'c', 'm', 'y', 'r', 'b', 'g', 'k', 'c', 'm',
                 'y'])

        labelled_diags = csr.actions.label_diags(labels, diags, fig_bbox)

        for diag in labelled_diags:

            label = diag.label
            diag.label = csr.actions.read_label(fig, label)
            diag = csr.r_group.detect_r_group(diag)
            csr.extract.get_smiles(diag, smiles, r_smiles)

            if debug is True:
                colour = next(colours)

                diag_rect = mpatches.Rectangle((diag.left, diag.top), diag.width, diag.height,
                                               fill=False, edgecolor=colour, linewidth=2)
                ax.text(diag.left, diag.top + diag.height / 4, '[%s]' % diag.tag, size=diag.height / 20, color='r')
                ax.add_patch(diag_rect)

                label_rect = mpatches.Rectangle((label.left, label.top), label.width, label.height,
                                                fill=False, edgecolor=colour, linewidth=2)
                ax.text(label.left, label.top + label.height / 4, '[%s]' % label.tag, size=label.height / 5, color='r')
                ax.add_patch(label_rect)

        if debug is True:
            ax.set_axis_off()
            plt.show()

        total_smiles = r_smiles + smiles

        return total_smiles

    def test_label_smile_resolution1(self):
        smiles = self.do_label_smile_resolution('S014372081630119X_gr1.jpg')
        print('extracted Smiles are : %s' % smiles)

        gold = [(['MeNAPH'],
                 'c1c(ccc(c1)N(c1ccc(/C=C/c2c3c(c(cc2)/C=C/c2ccc(N(c4ccc(C)cc4)c4ccc(cc4)C)cc2)cccc3)cc1)c1ccc(C)cc1)C'),
                (['MeONAPH'],
                 'c1c(ccc(c1)N(c1ccc(/C=C/c2c3c(c(cc2)/C=C/c2ccc(N(c4ccc(OC)cc4)c4ccc(cc4)OC)cc2)cccc3)cc1)c1ccc(OC)cc1)OC'),
                (['EtNAPH'], 'c1c2n(c3c(c2ccc1)cc(cc3)/C=C/c1ccc(/C=C/c2ccc3n(c4ccccc4c3c2)CC)c2c1cccc2)CC')]

        self.assertEqual(gold, smiles)

    def test_label_smile_resolution2(self):
        smiles = self.do_label_smile_resolution('S014372081630122X_gr1.jpg', debug=True)
        print('extracted Smiles are : %s' % smiles)

        # TODO : Try this with tesseract (label resolution is poor) - currently broken

        gold = [
            ['c1c(ccc(c1)N(c1ccc(/C=C/c2c3c(c(cc2)/C=C/c2ccc(N(c4ccc(C)cc4)c4ccc(cc4)C)cc2)cccc3)cc1)c1ccc(C)cc1)C',
             'c1c(ccc(c1)N(c1ccc(/C=C/c2c3c(c(cc2)/C=C/c2ccc(N(c4ccc(OC)cc4)c4ccc(cc4)OC)cc2)cccc3)cc1)c1ccc(OC)cc1)OC']]

        self.assertEqual(gold, smiles)

    def test_label_smile_resolution5(self):
        smiles = self.do_label_smile_resolution('S0143720816300201_sc2.jpg')
        print('extracted Smiles are : %s' % smiles)

        gold = [(['5(64%)'], 'n1(cccc1C=C(C#N)C#N)C'),
                (['8(74%)'], 'C1COc2c(O1)csc2C=C(C#N)C#N'),
                (['2(78%)'], 'n1(c2c(c3c1cccc3)cc(C=C(C#N)C#N)cc2)*'),
                (['3(86%)'], 'c1(N(C)C)ccc(cc1)C=C(C#N)C#N'),
                (['9(>99%)'], 'C[Fe]C1(C*CCC1)C'),  #  this will never pass as uses incompatible notation
                (['1(82%)'], 'c1c2Cc3cc(C=C(C#N)C#N)ccc3c2ccc1'),
                (['7(94%)'], 'c1ccc(s1)c1sc(cc1)C=C(C#N)C#N'),
                (['4(78%)'], 'o1cccc1C=C(C#N)C#N'),
                (['6(75%)'], 's1cccc1C=C(C#N)C#N')]

        self.assertEqual(gold, smiles)

    def test_label_smile_resolution6(self):
        smiles = self.do_label_smile_resolution('S0143720816300274_gr1.jpg')
        print('extracted Smiles are : %s' % smiles)

        gold = [(['7a'], 'CC(c1ccc(c2sc(c3c2[nH]c(n3)c2ccc(c3ccc(/C=C(\\C#N)/C(=O)O)cc3)cc2)c2ccc(C(C)(C)C)cc2)cc1)(C)C'),
            (['7b'], 'CC(c1ccc(c2sc(c3nc([nH]c23)c2ccc(c3sc(/C=C(\\C#N)/C(=O)O)cc3)cc2)c2ccc(C(C)(C)C)cc2)cc1)(C)C'),
            (['7c'], 'CC(c1ccc(c2sc(c3c2[nH]c(n3)c2sc(cc2)c2ccc(/C=C(\\C#N)/C(=O)O)s2)c2ccc(C(C)(C)C)cc2)cc1)(C)C'),
            (['8a'], 'c1(cccs1)c1sc(c2nc(n(c12)CCCC)c1ccc(c2ccc(/C=C(\\C#N)/C(=O)O)cc2)cc1)c1sccc1'),
            (['8b'], 'c1cc(sc1)c1sc(c2c1n(CCCC)c(n2)c1ccc(c2ccc(/C=C(\\C#N)/C(=O)O)s2)cc1)c1sccc1'),
            (['8c'], 's1c(c2sc(c3nc(n(c23)CCCC)c2sc(cc2)c2sc(cc2)/C=C(\\C#N)/C(=O)O)c2sccc2)ccc1')]

        self.assertEqual(gold, smiles)

    def test_label_smile_resolution7(self):
        smiles = self.do_label_smile_resolution('S0143720816300286_gr1.jpg')
        print('extracted Smiles are : %s' % smiles)

        gold = ['c1(N(C)C)ccc(cc1)C=C(C#N)C#N', 'n1(c2c(c3c1cccc3)cc(C=C(C#N)C#N)cc2)*',
                'c1c2Cc3cc(C=C(C#N)C#N)ccc3c2ccc1', 'o1cccc1C=C(C#N)C#N', 'n1(cccc1C=C(C#N)C#N)C',
                's1cccc1C=C(C#N)C#N', 'C[Fe]C1(C*CCC1)C', 'c1ccc(s1)c1sc(cc1)C=C(C#N)C#N']

        self.assertEqual(gold, smiles)

    def test_label_smile_resolution8(self):
        smiles = self.do_label_smile_resolution('S0143720816300419_sc1.jpg')
        print('extracted Smiles are : %s' % smiles)

        gold = [(['PDOF'], 'c12c3ccc(cc3C(=O)c2cc(cc1)c1ccc(C(=O)C)cc1)c1ccc(C(=O)C)cc1'),
            (['NDOF'], 'c12c3c(C(=O)c2cc(cc1)c1ccc(C(=O)OC)cc1)cc(c1ccc(C(=O)OC)cc1)cc3'),
            (['DDOF'], 'c12c3c(C(=O)c2cc(cc1)c1ccc(C=O)cc1)cc(c1ccc(C=O)cc1)cc3'),
            (['DPF'], 'c12c3c(C(=O)c2cc(c2ccccc2)cc1)cc(c1ccccc1)cc3')]

        self.assertEqual(gold, smiles)

    def test_label_smile_resolution9(self):
        smiles = self.do_label_smile_resolution('S0143720816300559_sc2.jpg')
        print('extracted Smiles are : %s' % smiles)

        gold = [(['3'], 'c1ccc2c(c1)nc(o2)c1c(O)c(OCC)c(c2oc3c(n2)cccc3)s1'),
            (['2'], 'c1ccc2c(c1)nc(o2)c1c(OCC)c(OCC)c(c2oc3c(n2)cccc3)s1'),
            (['1'], 'c1ccc2nc(oc2c1)c1c(O)c(O)c(c2oc3c(n2)cccc3)s1')]

        self.assertEqual(gold, smiles)

    def test_label_smile_resolution10(self):
        smiles = self.do_label_smile_resolution('S0143720816300821_gr2.jpg')
        print('extracted Smiles are : %s' % smiles)

        gold = [(['10'], 'c1(ccccc1)Nc1c2C(=O)c3ccccc3C(=O)c2c(Nc2cc(c(N)c3C(=O)c4c(C(=O)c23)cccc4)C)c(C)c1'),
            (['9'], 'c12ccccc1C(=O)c1c(Nc3c4C(=O)c5ccccc5C(=O)c4c(N)c(C)c3)c(C)ccc1C2=O')]

        self.assertEqual(gold, smiles)

    def test_label_smile_resolution11(self):
        smiles = self.do_label_smile_resolution('S0143720816300900_gr2.jpg')

        # TODO : Currently broken. Likely due to difficul-to-parse + and - signs in circles. Output contains wildcards and failures
        print('extracted Smiles are : %s' % smiles)

        gold = [(['lRDyeSOOCW'], 'C(C(=O)O)CCCCN1/C(=C/C=C\\2/C(=C(CCC2)/C=C/C2=[N](CCCCS(=O)(=O)O)c3c(C2(C)C)cc(cc3)S(=O)(=O)O)Oc2ccc(S(=O)(=O)OC)cc2)/C(C)(C)c2cc(S(=O)(=O)O)ccc12'),
            (['ZW800-1'], 'C(CC[N]1=C(/C=C/C2=C(Oc3ccc(CCC(=O)O)cc3)/C(=C/C=C\\3/N(CCC[N](=O)(C)(C)C)c4c(C3(C)C)cc(S(=O)(=O)O)cc4)/CCC2)C(c2c1ccc(S(=O)(=O)*)c2)(C)C)[N](C)(C)C'),
            (['Compound13'], 'S(=O)(=O)(CCC[N]1=C(/C=C/C2=C(c3ccc(CCC(=O)O)cc3)/C(=C/C=C\\3/N(CCCS(=O)(=O)O)c4c(C3(C)C)cc(S(=O)(=O)O)cc4)/CCC2)C(c2c1ccc(S(=O)(=O)O)c2)(C)C)O'),
            (['Compound10'], 'C(CCN1C(C(c2c1ccc1ccccc21)(C)C)/C=C/C1=C(c2ccc(CCC(=O)O)cc2)/C(=C/C=C\\2/N(CCCS(=O)(=O)O)c3c(C2(C)C)c2ccccc2cc3)/CCC1)S(=O)(=O)O'),
            (['Compound11'], 'S(=O)(=O)(CCC[N]1=C(/C=C/C2=C(c3ccc(CCC(=O)O)cc3)/C(=C/C=C\\3/N(CCCS(=O)(=O)*)c4c(C3(C)C)cccc4)/CCC2)C(c2c1cccc2)(C)C)O'),
            (['Compound12'], 'C1C(=C(c2ccc(CCC(=O)O)cc2)/C(=C/C=C/2\\C(C)(C)c3cc(S(=O)(=O)*)ccc3N2C)/CC1)/C=C/C1=[N](c2c(C1(C)C)cc(cc2)S(=O)(=O)*)C'),
            (['ICG'], 'C(CCC[N]1=C(C(c2c3c(ccc12)cccc3)(C)C)/C=C/CC(/C=C/C=C\\1/N(CCCCS(=O)(=O)O)c2c(C1(C)C)c1ccccc1cc2)C)S(=O)(=O)O')]

        self.assertEqual(gold, smiles)

    def test_label_smile_resolution12(self):
        # TODO : This diagram still fails in resolving the : in the label of R-group diagram
        smiles = self.do_label_smile_resolution('S0143720816301115_r75.jpg')
        print('extracted Smiles are : %s' % smiles)

        gold = [([], 'C1=C2C3C(=CC=C2)C=Cc2cc(c(O)c(C1)c32)/C=N\\CC*CC/N=C\\c1cc2ccc3c4c(ccc3)ccc(c1O)c24'),
            ([], 'C1=C2C3C(=CC=C2)C=Cc2cc(c(O)c(C1)c32)/C=N\\CC*CC/N=C\\c1cc2ccc3c4c(ccc3)ccc(c1O)c24'),
            (['107'], 'c1c2ccc3cccc4c3c2c(cc4)cc1/C=N/CCSSCC/N=C/c1cc2ccc3cccc4ccc(c1)c2c34'),
            (['106'], 'c1c2cccc3ccc4c(c(cc(c1)c4c23)/C=N/c1ccccc1O)O')]

        self.assertEqual(gold, smiles)

    def test_label_smile_resolution13(self):
        smiles = self.do_label_smile_resolution('S0143720816301681_gr1.jpg')
        print('extracted Smiles are : %s' % smiles)

        gold = [(['1'], 'N(CC)(CC)c1ccc2cc(C#N)c(=N)oc2c1'),
            (['2'], 'N(CC)(CC)c1ccc2cc(C#N)/c(=N/C(=O)OCC)/oc2c1'),
            (['3'], 'N(CC)(CC)c1ccc2cc(C#N)c(=O)oc2c1'),
            (['4'], 'N(CC)(CC)c1ccc2ccc(=O)oc2c1')]

        self.assertEqual(gold, smiles)

    def test_label_smile_resolution14(self):
        smiles = self.do_label_smile_resolution('S0143720816301115_gr4.jpg')
        print('extracted Smiles are : %s' % smiles)

        gold = [(['14:1-isoTQTACN'], 'n1ccc2c(c1CN1CCN(Cc3nccc4ccccc34)CCN(CC1)Cc1c3ccccc3ccn1)cccc2'),
            (['11'], 'c1cc(nc2c1cccc2)CN1CCN(Cc2nc3c(cc2)cccc3)CCN(CC1)Cc1ccc2ccccc2n1'),
            (['15:6-MeOTQTACN'], 'c1c(cc2c(c1)nc(cc2)CN1CCN(Cc2nc3c(cc2)cc(OC)cc3)CCN(CC1)Cc1ccc2cc(OC)ccc2n1)OC'),
            (['12'], 'N1CCNCCN(CC1)Cc1ccc2ccccc2n1'),
            (['13'], 'C(N1CCN(Cc2nc3ccccc3cc2)CCSCC1)c1nc2c(cc1)cccc2')]

        self.assertEqual(gold, smiles)

    def test_label_smile_resolution15(self):
        # Currently broken - need to improve resolution of colons

        smiles = self.do_label_smile_resolution('S0143720816301115_gr1.jpg')
        print('extracted Smiles are : %s' % smiles)

        gold = [(['1'], '*c1c2ccc(CN(CCN(Cc3nc4cc(c(c(c4cc3)*)*)*)Cc3nc4c(cc3)c(c(c(c4)*)*)*)Cc3ccc4c(*)c(*)c(*)cc4n3)nc2cc(*)c1*')
            ([], '*c1c2ccc(CN(CCN(Cc3nc4cc(c(c(c4cc3)*)*)*)Cc3nc4c(cc3)c(c(c(c4)*)*)*)Cc3ccc4c(*)c(*)c(*)cc4n3)nc2cc(*)c1*'),
            (['3', 'T(TMQ)EN'], '*c1c2ccc(CN(CCN(Cc3nc4cc(c(c(c4cc3)*)OC)*)Cc3nc4c(cc3)c(c(c(c4)*)OC)*)Cc3ccc4c(*)c(OC)c(*)cc4n3)nc2cc(*)c1OC')]

        self.assertEqual(gold, smiles)

    def do_osra(self, filename):
        """ Tests the OSRA chemical diagram recognition """

        test_diag = os.path.join(examples_dir, filename)

        # Read in float and raw pixel images
        fig = csr.io.imread(test_diag)
        raw_fig = csr.io.imread(test_diag, raw=True)

        # Create unreferenced binary copy
        bin_fig = copy.deepcopy(fig)

        panels = csr.actions.segment(bin_fig)
        panels = csr.actions.preprocessing(panels, bin_fig)

        # Create output image
        out_fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(fig.img)

        diags, labels = csr.actions.classify_kruskal(panels)
        labelled_diags = csr.actions.label_kruskal(diags, labels)

        colours = iter(
            ['r', 'b', 'g', 'k', 'c', 'm', 'y', 'r', 'b', 'g', 'k', 'c', 'm', 'y', 'r', 'b', 'g', 'k', 'c', 'm',
             'y'])

        smiles = []

        for diag in labelled_diags:
            colour = next(colours)

            diag_rect = mpatches.Rectangle((diag.left, diag.top), diag.width, diag.height,
                                           fill=False, edgecolor=colour, linewidth=2)
            ax.text(diag.left, diag.top + diag.height / 4, '[%s]' % diag.tag, size=diag.height / 20, color='r')
            ax.add_patch(diag_rect)

            label = diag.label
            label_rect = mpatches.Rectangle((label.left, label.top), label.width, label.height,
                                            fill=False, edgecolor=colour, linewidth=2)
            ax.text(label.left, label.top + label.height / 4, '[%s]' % label.tag, size=label.height / 5, color='r')
            ax.add_patch(label_rect)

            smile, confidence = csr.actions.read_diagram(fig, diag)
            if '*' not in smile:
                print(smile, confidence)
            smiles.append(smile)
            print("Label {} ({}): {} ".format(diag.tag, confidence, smile))


        ax.set_axis_off()
        plt.savefig(os.path.join(labelled_output_dir, filename))

        return smiles

    def test_osra2(self):
        smiles = self.do_osra('S014372081630122X_gr1.jpg')
        print(smiles)

        """ Output with .jpg on 300dpi
        Label 4 (7.9463): N#C/C(=C\c1ccc(s1)c1ccc(c2c1*=C(*)C(=*2)**)c1ccc(s1)c1ccc(cc1)*(c1ccc(cc1)*)c1ccc(cc1)*)/C(=O)O 
Label 1 (5.9891): N#C/C(=C\c1ccc(s1)c1ccc(c2c1nc(**)c(n2)*)c1ccc(s1)c1ccc(cc1)*(c1ccccc1)c1ccccc1)/C(=O)O 
Label 5 (6.1918): N#C/C(=C\c1ccc(s1)c1cc(*)c(cc1*)c1ccc(s1)c1ccc(cc1)N(c1ccccc1)c1ccccc1)/C(=O)O 
Label 0 (9.4724): CCCCCCc1nc2c(c3ccc(s3)/C=C(/C(=O)O)\C#N)c3*=C(**)C(=*c3c(c2nc1*)c1ccc(s1)c1ccc(cc1)N(c1ccccc1)c1ccccc1)** """

    def test_osra3(self):
        smiles = self.do_osra('S014372081630167X_sc1.jpg')
        print(smiles)

    def test_osra5(self):
        smiles = self.do_osra('S0143720816300201_sc2.jpg')
        print(smiles)


    def test_osra6(self):
        smiles = self.do_osra('S0143720816300274_gr1.jpg')
        print(smiles)

    def test_osra7(self):
        smiles = self.do_osra('S0143720816300419_sc1.jpg')
        print(smiles)

    def test_osra8(self):
        smiles = self.do_osra('S0143720816300559_sc2.jpg')
        print(smiles)

    def test_osra9(self):
        smiles = self.do_osra('S0143720816300821_gr2.jpg')
        print(smiles)

    def test_osra10(self):
        # IR dye doesn't work
        smiles= self.do_osra('S0143720816300900_gr2.jpg')
        print(smiles)


class TestValidation(unittest.TestCase):

    def do_metrics(self, filename):
        """ Used to identify correlations between metrics and output validity"""

        test_fig = os.path.join(examples_dir, filename)

        # Read in float and raw pixel images
        fig = csr.io.imread(test_fig)
        raw_fig = csr.io.imread(test_fig, raw=True)

        # Create unreferenced binary copy
        bin_fig = copy.deepcopy(fig)

        panels = csr.actions.segment(bin_fig)
        panels = csr.actions.preprocessing(panels, fig)

        # Create output image
        out_fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(fig.img)

        diags, labels = csr.actions.classify_kruskal(panels)
        labelled_diags = csr.actions.label_kruskal(diags, labels)

        colours = iter(
            ['r', 'b', 'g', 'k', 'c', 'm', 'y', 'r', 'b', 'g', 'k', 'c', 'm', 'y', 'r', 'b', 'g', 'k', 'c', 'm',
             'y'])

        smiles = []

        avg_pixel_ratio = csr.validate.total_pixel_ratio(bin_fig, labelled_diags)
        diags_to_image_ratio = csr.validate.diagram_to_image_area_ratio(bin_fig, labelled_diags)
        avg_diag_area_to_total_img_ratio = csr.validate.avg_diagram_area_to_image_area(bin_fig, labelled_diags)

        for diag in labelled_diags:
            colour = next(colours)

            diag_rect = mpatches.Rectangle((diag.left, diag.top), diag.width, diag.height,
                                           fill=False, edgecolor=colour, linewidth=2)
            ax.text(diag.left, diag.top + diag.height / 4, '[%s]' % diag.tag, size=diag.height / 20, color='r')
            ax.add_patch(diag_rect)

            label = diag.label
            label_rect = mpatches.Rectangle((label.left, label.top), label.width, label.height,
                                            fill=False, edgecolor=colour, linewidth=2)
            ax.text(label.left, label.top + label.height / 4, '[%s]' % label.tag, size=label.height / 5, color='r')
            ax.add_patch(label_rect)

            smile, confidence = csr.actions.read_diagram(fig, diag)
            smiles.append(smile)
            print("Label {} ({}): {} ".format(diag.tag, confidence, smile))
            print("Black pixel ratio : %s " % csr.validate.pixel_ratio(bin_fig, diag))

        print('Overall diagram metrics:')
        print('Average 1 / all ratio: %s' % avg_pixel_ratio)
        print('Average diag / fig area ratio: %s' % avg_diag_area_to_total_img_ratio)
        print('Diag number to fig area ratio: %s' % diags_to_image_ratio)


        ax.set_axis_off()
        plt.savefig(os.path.join(labelled_output_dir, filename))

        return smiles

    def test_validation2(self):
        smiles = self.do_metrics('S014372081630122X_gr1.jpg')

    def test_validation3(self):
        smiles = self.do_metrics('S014372081630167X_sc1.jpg')

    def test_validation5(self):
        smiles = self.do_metrics('S0143720816300201_sc2.jpg')

    def test_validation6(self):
        smiles = self.do_metrics('S0143720816300274_gr1.jpg')

    def test_validation7(self):
        smiles = self.do_metrics('S0143720816300419_sc1.jpg')

    def test_validation8(self):
        smiles = self.do_metrics('S0143720816300559_sc2.jpg')

    def test_validation9(self):
        smiles = self.do_metrics('S0143720816300821_gr2.jpg')

    def test_validation10(self):
        # IR dye doesn't work
        smiles= self.do_metrics('S0143720816300900_gr2.jpg')


class TestFiltering(unittest.TestCase):
    """ Tests the results filtering via wildcard removal and pybel validation """

    def do_filtering(self, filename):
        """ Used to identify correlations between metrics and output validity"""
        test_fig = os.path.join(examples_dir, filename)

        # Read in float and raw pixel images
        fig = csr.io.imread(test_fig)
        raw_fig = csr.io.imread(test_fig, raw=True)

        # Create unreferenced binary copy
        bin_fig = copy.deepcopy(fig)

        # Preprocessing steps
        panels = csr.actions.segment(bin_fig)
        panels = csr.actions.preprocessing(panels, fig)

        # Create output image
        out_fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(fig.img)

        # Get label pairs
        diags, labels = csr.actions.classify_kruskal(panels)
        labelled_diags = csr.actions.label_kruskal(diags, labels)

        colours = iter(
            ['r', 'b', 'g', 'k', 'c', 'm', 'y', 'r', 'b', 'g', 'k', 'c', 'm', 'y', 'r', 'b', 'g', 'k', 'c', 'm',
                'y'])

        diags_with_smiles = []

        for diag in labelled_diags:
            colour = next(colours)

            diag_rect = mpatches.Rectangle((diag.left, diag.top), diag.width, diag.height,
                                            fill=False, edgecolor=colour, linewidth=2)
            ax.text(diag.left, diag.top + diag.height / 4, '[%s]' % diag.tag, size=diag.height / 20, color='r')
            ax.add_patch(diag_rect)

            label = diag.label
            label_rect = mpatches.Rectangle((label.left, label.top), label.width, label.height,
                                            fill=False, edgecolor=colour, linewidth=2)
            ax.text(label.left, label.top + label.height / 4, '[%s]' % label.tag, size=label.height / 5, color='r')
            ax.add_patch(label_rect)

            smile, confidence = csr.actions.read_diagram(fig, diag)
            diag.smile = smile
            diags_with_smiles.append(diag)

        # Run post-processing: 
        formatted_smiles = csr.validate.format_all_smiles(diags_with_smiles)
        print(formatted_smiles)
        return formatted_smiles

    def test_filtering2(self):
        smiles = self.do_filtering('S014372081630122X_gr1.jpg')

    def test_filtering3(self):
        smiles = self.do_filtering('S014372081630167X_sc1.jpg')

    def test_filtering5(self):
        smiles = self.do_filtering('S0143720816300201_sc2.jpg')

    def test_filtering6(self):
        smiles = self.do_filtering('S0143720816300274_gr1.jpg')

    def test_filtering7(self):
        smiles = self.do_filtering('S0143720816300419_sc1.jpg')

    def test_filtering8(self):
        smiles = self.do_filtering('S0143720816300559_sc2.jpg')

    def test_filtering9(self):
        smiles = self.do_filtering('S0143720816300821_gr2.jpg')

    def test_filtering10(self):
        # IR dye doesn't work
        smiles= self.do_filtering('S0143720816300900_gr2.jpg')