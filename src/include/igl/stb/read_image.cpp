// This file is part of libigl, a simple c++ geometry processing library.
//
// Copyright (C) 2016 Daniele Panozzo <daniele.panozzo@gmail.com>
//
// This Source Code Form is subject to the terms of the Mozilla Public License
// v. 2.0. If a copy of the MPL was not distributed with this file, You can
// obtain one at http://mozilla.org/MPL/2.0/.
#include "read_image.h"
#include <stb_image.h>

IGL_INLINE bool igl::stb::read_image(
  const std::string image_file,
  Eigen::Matrix<unsigned char,Eigen::Dynamic,Eigen::Dynamic>& R,
  Eigen::Matrix<unsigned char,Eigen::Dynamic,Eigen::Dynamic>& G,
  Eigen::Matrix<unsigned char,Eigen::Dynamic,Eigen::Dynamic>& B,
  Eigen::Matrix<unsigned char,Eigen::Dynamic,Eigen::Dynamic>& A
)
{
  int cols,rows,n;
  unsigned char *data = stbi_load(image_file.c_str(), &cols, &rows, &n, 4);
  if(data == NULL) {
    return false;
  }

  R.resize(cols,rows);
  G.resize(cols,rows);
  B.resize(cols,rows);
  A.resize(cols,rows);

  for (unsigned i=0; i<rows; ++i) {
    for (unsigned j=0; j<cols; ++j) {
      R(j,rows-1-i) = data[4*(j + cols * i) + 0];
      G(j,rows-1-i) = data[4*(j + cols * i) + 1];
      B(j,rows-1-i) = data[4*(j + cols * i) + 2];
      A(j,rows-1-i) = data[4*(j + cols * i) + 3];
    }
  }

  stbi_image_free(data);

  return true;
}

#ifdef IGL_STATIC_LIBRARY
// Explicit template instantiation
// generated by autoexplicit.sh
#endif
