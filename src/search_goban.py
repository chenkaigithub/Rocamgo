#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Rocamgo is recogniter of the go games by processing digital images with opencv.
# Copyright (C) 2012 Víctor Ramirez de la Corte <virako.9 at gmail dot com>
# Copyright (C) 2012 David Medina Velasco <cuidadoconeltecho at gmail dot com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from cv import Canny
from cv import Smooth
from cv import CreateMat
from cv import CreateMemStorage
from cv import CreateImage
from cv import FindContours
from cv import CV_RETR_TREE
from cv import CV_CHAIN_APPROX_NONE
from cv import CV_POLY_APPROX_DP
from cv import CV_RGB2GRAY
from cv import ContourArea
from cv import IPL_DEPTH_8U
from cv import CvtColor
from cv import GetMat
from cv import CV_GAUSSIAN
from cv import ApproxPoly
from math import sqrt
from src.cte import NUM_EDGES

def count_perimeter(seq):
    """Contamos el perímetro de una secuencia dada. 

    :Param seq: secuencia de puntos
    :Type seq: CvSeq
    :Return: distancia del perímetro
    :Rtype: float
    """
    ant = False
    perimeter = 0
    for (a,b) in seq:
        if ant:
            perimeter += sqrt((ant[0]-a)**2 + (ant[1]-b)**2)
        else:
            perimeter = sqrt((seq[-1][0]-a)**2 + (seq[-1][1]-b)**2)
        ant = (a,b)
    return perimeter

def get_corners(contour):
    """Hallamos las esquinas a partir de un contorno y las ordenamos de la siguiente manera: ul, dl, ur, dr.  u = up, l = left, d = down, r = right.

    :Param contour: contorno del tablero obtenido
    :Type contour: CvSeq
    :Return: lista de esquinas
    :Rtype: list """
    corners = []
    for (x,y) in contour:
        corners.append((x,y))
    corners.sort()
    c1 = corners[:2]
    c2 = corners[2:]
    if corners[0][1] >= corners[1][1]:
        c1.reverse()
    if corners[2][1] >= corners[3][1]:
        c2.reverse()
    return c1 + c2


def filter_image(img):
    """Aplicamos unos filtros a las imágenes para facilitar su tratamiento. Buscamos contornos y suavizamos. 

    :Param img: imagen sin filtrar
    :Type img: CvMat
    :Return: imagen filtrada
    :Rtype: CvMat """
    aux_1 = CreateMat(img.rows, img.cols, img.type)
    aux_2 = CreateMat(img.rows, img.cols, img.type)
    Canny(img, aux_2, 50, 200, 3)
    Smooth(aux_2, aux_1, CV_GAUSSIAN, 3, 3)
    return aux_1


def detect_contour(img):
    """Buscamos contornos con unas características determinadas para encontrar un tablero de go en una imagen. 

    :Param img: imagen filtrada para buscar contornos en ella
    :Type img: CvMat
    :Return: Contorno si no lo encuentra, sino None
    :Rtype: CvSeq """
    storage = CreateMemStorage()
    seq = FindContours(img, storage, CV_RETR_TREE, CV_CHAIN_APPROX_NONE, 
      offset=(0, 0))
    sequence = []
    
    aprox = True
    while seq:
        if len(seq) >= NUM_EDGES and (img.cols*img.rows) > ContourArea(seq) > \
            ((img.cols/2)*(img.rows/2)):
            perimeter = count_perimeter(seq)
            seq_app = ApproxPoly(seq, storage, CV_POLY_APPROX_DP, perimeter*0.02, 1)
            if len(seq_app) == NUM_EDGES:
                return seq_app
            else:
                return None
        else:
            if seq.h_next() == None:
                break
            else:
                seq = seq.h_next()
    return None


def search_goban(img): 
    """Busca el tablero en una imagen. 

    :Param img: imagen del tablero
    :Type img: IplImage # TODO comprobar tipo imagen
    :Return: lista de esquinas si las encuentra, sino None
    :Rtype: list or None """
    aux_gray = CreateImage((img.width, img.height), IPL_DEPTH_8U, 1)
    CvtColor(img, aux_gray, CV_RGB2GRAY)
    img_gray = GetMat(aux_gray, 0)
    img_filtered = filter_image(img_gray)
    contour = detect_contour(img_filtered)
    if contour: 
        return get_corners(contour)
    else:
        return None

