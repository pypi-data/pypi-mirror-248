/* approx.f -- translated by f2c (version 19980913).
   You must link the resulting object file with the libraries:
	-lf2c -lm   (in that order)
*/

#include "f2c.h"

/* $Procedure APPROX ( Approximate equality ) */
logical approx_(doublereal *x, doublereal *y, doublereal *tol)
{
    /* System generated locals */
    doublereal d__1;
    logical ret_val;

/* $ Abstract */

/*     Return .TRUE. if two double precision numbers are equal to */
/*     within some tolerance. */

/* $ Disclaimer */

/*     THIS SOFTWARE AND ANY RELATED MATERIALS WERE CREATED BY THE */
/*     CALIFORNIA INSTITUTE OF TECHNOLOGY (CALTECH) UNDER A U.S. */
/*     GOVERNMENT CONTRACT WITH THE NATIONAL AERONAUTICS AND SPACE */
/*     ADMINISTRATION (NASA). THE SOFTWARE IS TECHNOLOGY AND SOFTWARE */
/*     PUBLICLY AVAILABLE UNDER U.S. EXPORT LAWS AND IS PROVIDED "AS-IS" */
/*     TO THE RECIPIENT WITHOUT WARRANTY OF ANY KIND, INCLUDING ANY */
/*     WARRANTIES OF PERFORMANCE OR MERCHANTABILITY OR FITNESS FOR A */
/*     PARTICULAR USE OR PURPOSE (AS SET FORTH IN UNITED STATES UCC */
/*     SECTIONS 2312-2313) OR FOR ANY PURPOSE WHATSOEVER, FOR THE */
/*     SOFTWARE AND RELATED MATERIALS, HOWEVER USED. */

/*     IN NO EVENT SHALL CALTECH, ITS JET PROPULSION LABORATORY, OR NASA */
/*     BE LIABLE FOR ANY DAMAGES AND/OR COSTS, INCLUDING, BUT NOT */
/*     LIMITED TO, INCIDENTAL OR CONSEQUENTIAL DAMAGES OF ANY KIND, */
/*     INCLUDING ECONOMIC DAMAGE OR INJURY TO PROPERTY AND LOST PROFITS, */
/*     REGARDLESS OF WHETHER CALTECH, JPL, OR NASA BE ADVISED, HAVE */
/*     REASON TO KNOW, OR, IN FACT, SHALL KNOW OF THE POSSIBILITY. */

/*     RECIPIENT BEARS ALL RISK RELATING TO QUALITY AND PERFORMANCE OF */
/*     THE SOFTWARE AND ANY RELATED MATERIALS, AND AGREES TO INDEMNIFY */
/*     CALTECH AND NASA FOR ALL THIRD-PARTY CLAIMS RESULTING FROM THE */
/*     ACTIONS OF RECIPIENT IN THE USE OF THE SOFTWARE. */

/* $ Required_Reading */

/*     None. */

/* $ Keywords */

/*     COMPARE */
/*     NUMBERS */

/* $ Declarations */
/* $ Brief_I/O */

/*     VARIABLE  I/O  DESCRIPTION */
/*     --------  ---  -------------------------------------------------- */
/*     X, */
/*     Y          I   Double precision numbers. */
/*     TOL        I   Tolerance. */

/*     The function is .TRUE. whenever |X - Y| <= TOL. */

/* $ Detailed_Input */

/*     X, */
/*     Y        are arbitrary double precision numbers. */

/*     TOL      is a tolerance. X and Y are considered to be equal */
/*              if they differ by no more than this amount. If TOL */
/*              is negative, X and Y are never considered equal. */

/* $ Detailed_Output */

/*     The function is .TRUE. whenever |X - Y| <= TOL, and is .FALSE. */
/*     otherwise. */

/* $ Parameters */

/*     None. */

/* $ Exceptions */

/*     Error free. */

/* $ Files */

/*     None. */

/* $ Particulars */

/*     None. */

/* $ Examples */

/*     C */
/*     C     If the eccentricity is near one, this a parabola. */
/*     C */
/*           IF ( APPROX ( ECC, 1.D0, 10.D-12 ) ) THEN */
/*              TYPE = 'PARABOLA' */

/*           ELSE IF ( ECC .LT. 1 ) THEN */
/*              TYPE = 'ELLIPSE' */

/*           ELSE */
/*              TYPE = 'HYPERBOLA' */
/*           END IF */

/* $ Restrictions */

/*     None. */

/* $ Literature_References */

/*     None. */

/* $ Author_and_Institution */

/*     J. Diaz del Rio    (ODC Space) */
/*     W.L. Taber         (JPL) */
/*     I.M. Underwood     (JPL) */

/* $ Version */

/* -    SPICELIB Version 1.1.0, 26-OCT-2021 (JDR) */

/*        Added IMPLICIT NONE statement. */

/*        Edited the header to comply with NAIF standard. */

/* -    SPICELIB Version 1.0.1, 10-MAR-1992 (WLT) */

/*        Comment section for permuted index source lines was added */
/*        following the header. */

/* -    SPICELIB Version 1.0.0, 31-JAN-1990 (IMU) */

/* -& */
/* $ Index_Entries */

/*     approximate equality */

/* -& */

/*     Just shorthand, really. */

    ret_val = (d__1 = *x - *y, abs(d__1)) <= *tol;
    return ret_val;
} /* approx_ */

